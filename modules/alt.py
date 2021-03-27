#This module is used to find alternative folders or files
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys
import random
import string
import itertools

class Alt(IPlugin):

    def __init__(self):
        self.requestList = [] #Store generated request objects

    def generate_alts(self,length=3):
        altlist = []
        chars = string.ascii_letters + string.digits + '_-'
        for item in itertools.product(chars, repeat=length):
            word = "".join(item)
            altlist.append(word)
        return altlist

    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module, datalist):
        length = 3
        if datalist != None:
            length = int(datalist[0])
            if length > 3:
                length = 3
            finalalt = []
            for i in range(1,length+1):
                alts = []
                alts = self.generate_alts(i)
                for j in alts:
                    finalalt.append(j)
        else:
            print('alt: Specify where to inject with *@* using -dl [1-3]')
            sys.exit(0)


        #Used to track if fuzz string is used
        isvalid = 0

        for fuzz in finalalt:
            newrls = []
            for u in urls:
                #==Replace url data==
                if '*@*' in u:
                    isvalid += 1
                    newrl = u.replace('*@*',fuzz)
                    newrls.append(newrl)
                
                #==Replace headers data==
                if len(headers) > 0:
                    newheaders = {}
                    for h,v in headers.items():
                        h1 = h
                        v1 = v
                        if '*@*' in h:
                            isvalid += 1
                            h1 = h.replace('*@*',fuzz)
                        if '*@*' in v:
                            isvalid += 1
                            v1 = v.replace('*@*',fuzz)
                        newheaders[h1]=v1
                else:
                    newheaders = headers

                #==Replace cookies data==
                if len(cookies) > 0:
                    newcookies = {}
                    for c,v in cookies.items():
                        c1 = c
                        v1 = v
                        if '*@*' in c:
                            isvalid += 1
                            c1 = c.replace('*@*', fuzz)
                        if '*@*' in v:
                            isvalid += 1
                            v1 = v.replace('*@*', fuzz)
                        newcookies[c1]=v1
                else:
                    newcookies = cookies

                #==Replace post data==
                if len(postdata) > 0:
                    newpostdata = {}
                    for p,v in postdata.items():
                        p1 = p
                        v1 = v
                        if '*@*' in p:
                            isvalid += 1
                            p1 = p.replace('*@*', fuzz)
                        if '*@*' in v:
                            isvalid += 1
                            v1 = v.replace('*@*', fuzz)
                        newpostdata[p1]=v1
                else:
                    newpostdata = postdata

            if isvalid > 0:
                for url in newrls:
                    if len(postdata) > 0:
                        req_post = RequestObject('reqID','POST', proxy, newheaders,
                                                    timeout, newcookies, url,
                                                    newpostdata, module)
                        self.requestList.append(req_post)

                    else:
                        req_get = RequestObject('reqID', 'GET', proxy, newheaders,
                                                timeout, newcookies, url,
                                                newpostdata, module)
                        self.requestList.append(req_get)
            else:
                print('alt: Specify where to inject with *@* using -dl [1-3]')
                sys.exit(0)

        return self.requestList
