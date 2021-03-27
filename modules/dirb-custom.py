#This module is used to directory bust for a user provided list
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys

class DirbCustom(IPlugin):
    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module, datalist):
        requestList = []   #Store generated request objects
        try:
            data = FileOp(datalist[0]).reader()
        except:
            print('dirb-custom: Provide a wordlist using -dl [wordlist]')
            sys.exit(0)
        for url in urls:
            u = UrlObject(url)
            for directory in data:
                newurl = u.u_d + directory
                req_get = RequestObject('reqID',"GET", proxy, headers, 
                                        timeout, cookies, newurl, postdata,
                                        module)
                requestList.append(req_get)
        return requestList
