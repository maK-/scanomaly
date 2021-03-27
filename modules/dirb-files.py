#This module is used to directory bust for sepcified common file types
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject

class DirbFile(IPlugin):
    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module, datalist):
        requestList = []   #Store generated request objects
        data = FileOp(cwd+'/lists/files.xtcz').reader()
        db = ''
        print('file extension: '+str(datalist))
        for url in urls:
            u = UrlObject(url)
            for ftype in datalist:
                for directory in data:
                    newurl = u.u_d + directory.replace('xtcz', ftype)
                    req_get = RequestObject('reqID',"GET", proxy, headers, 
                                            timeout, cookies, newurl, postdata,
                                            module)
                    requestList.append(req_get)
        return requestList
