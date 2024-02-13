#This module is used to brute force parameters
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import copy

class Parameth(IPlugin):

    def getParamStr(self, reqdata):
        dataString = ''
        if len(reqdata) != 0:
            for i,j in reqdata.items():
                dataString += i + '=' + j
                dataString += '&'
        return dataString[:-1]

    def gen(self, reqs, module, rules):
        requestList = []   #Store generated request objects
        params = FileOp(rules['cwd']+'/lists/parameters.txt').reader()
       
        paramValue = 'discobiscuits'

        db = ''
        for req in reqs:
            u = UrlObject(req.url)
            #Brute GET and POST Parameters
            for param in params:
                req_get = copy.deepcopy(req)
                ndata = req.data.copy()
                ndata[param] = paramValue
                haxgod = u.u_q + '?' + self.getParamStr(ndata)
                req_get.update_url(haxgod)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

                req_post = copy.deepcopy(req_get)
                req_post.update_url(req.url)
                req_post.update_data(ndata)
                req_post.update_method('POST')
                requestList.append(req_post)
                del ndata[param]

        return requestList
