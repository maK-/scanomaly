#This module is used to fuzz all request parameters
#With user provided payloads
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import copy
import sys

class Fuzz(IPlugin):
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
        headers = FileOp(rules['cwd']+'/lists/all-headers.txt').reader() 

        if len(rules['datalist']) == 0:
            print('fuzz: -dl [fuzz payload] [fuzz payload] ...')
            sys.exit(0)

        for fuzz in rules['datalist']:
            paramValue = fuzz
            headerValue = fuzz
            db = ''
            for req in reqs:
                u = UrlObject(req.url)

                #Brute all headers with fuzzstrings
                for head in headers:
                    req_head = copy.deepcopy(req)
                    heads = req.headers.copy()
                    heads[head] = headerValue
                    req_head.update_headers(heads)
                    req_head.update_reqID('reqID')
                    req_head.update_module(module)
                    requestList.append(req_head)
                    del heads[head]
                
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
            
            #Add custom fuzz to path
            for req in reqs:
                u = UrlObject(req.url)
                newurl = u.u_d+paramValue
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

            #Add custom fuzz to path+?
            for req in reqs:
                u = UrlObject(req.url)
                newurl = u.u_d+'?'+paramValue
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

            #Included headers coverage (like user agent etc)
            for req in reqs:
                req_head = copy.deepcopy(req)
                heads = req.headers.copy()
                newhead = copy.deepcopy(heads)
                for h,value in heads.items():
                    req_head2 = copy.deepcopy(req)
                    newhead[h] = headerValue           
                    req_head2.update_headers(heads)                               
                    req_head2.update_reqID('reqID')                               
                    req_head2.update_module(module)                               
                    requestList.append(req_head2)                                 
                    del newhead[h]

        return requestList
