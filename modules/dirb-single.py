#This module is used to directory bust for a user provided list
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys

class DirbSingle(IPlugin):
    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module, datalist):
        requestList = []   #Store generated request objects
        for url in urls:
            u = UrlObject(url)
            for dirs in datalist:
                newurl = u.u_d + dirs
                req_get = RequestObject('reqID',"GET", proxy, headers, 
                                        timeout, cookies, newurl, postdata,
                                        module)
                requestList.append(req_get)
                print(requestList)
        return requestList
