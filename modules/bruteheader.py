#This module is used to brute force HTTP Headers
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
        headers = FileOp(rules['cwd']+'/lists/all-headers.txt').reader()
       
        headerValues = ['discobiscuits', '127.0.0.1']

        db = ''
        for req in reqs:
            u = UrlObject(req.url)

            #Brute Request Headers
            for head in headers:
                for headerValue in headerValues:
                    req_head = copy.deepcopy(req)
                    heads = req.headers.copy()
                    heads[head] = headerValue
                    req_head.update_headers(heads)
                    req_head.update_reqID('reqID')
                    req_head.update_module(module)
                    requestList.append(req_head)
                    del heads[head]
        return requestList
