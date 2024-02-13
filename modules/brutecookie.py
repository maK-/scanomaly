#This module is used to brute force cookies
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
       
        paramValues = ['discobiscuits','%00','%0d%0a', '']
        db = ''
        for req in reqs:
            #Brute Cookies
            for cookie in params:
                for paramValue in paramValues:
                    req_c = copy.deepcopy(req)
                    monster = req.cookies.copy()
                    monster[cookie] = str(paramValue)
                    req_c.update_cookies(monster)
                    req_c.update_reqID('reqID')
                    req_c.update_module(module)
                    requestList.append(req_c)
                    del monster[cookie]
        return requestList
