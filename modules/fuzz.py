#This module is used to fuzz requests (with or without a provided list)
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys

class Fuzz(IPlugin):
    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module, datalist):
        requestList = []   #Store generated request objects
        try:
            data = FileOp(datalist[0]).reader()
        except:
            data = FileOp(cwd+'/lists/known-fuzz.txt').reader()
        
        #Used to track if fuzz string is used
        isvalid = 0

        for fuzz in data:

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
                        requestList.append(req_post)

                    else:
                        req_get = RequestObject('reqID', 'GET', proxy, newheaders,
                                                timeout, newcookies, url,
                                                newpostdata, module)
                        requestList.append(req_get)
            else:
                print('fuzz: Specify where with *@* and provide a wordlist using -dl [wordlist]')
                sys.exit(0)

        return requestList
