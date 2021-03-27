#This module is used to fuzz requests in multiple locations
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import urllib.parse
import sys, copy

class FuzzAll(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []   #Store generated request objects
        payloads = FileOp(rules['cwd']+'/lists/known-fuzz.txt').reader()
        for req in reqs:
            for fuzz in payloads:
                fuzz_encoded = urllib.parse.quote(fuzz)

                #Fuzz all GET and POST parameters a=*fuzz*, b=*fuzz*
                params = req.data.copy()
                for param in params.keys():
                    req_get = copy.deepcopy(req)
                    data = req.data.copy()
                    data[param] = fuzz
                    req_get.update_data(data)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

                #Fuzz all GET and POST parameters a=value*fuzz*,b=value*fuzz*
                for param in params.keys():
                    req_get = copy.deepcopy(req)
                    data = req.data.copy()
                    value = data[param]
                    data[param] = value + fuzz
                    req_get.update_data(data)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

                #Fuzz all cookies
                cookies = req.cookies.copy()
                for cookie in cookies.keys():
                    req_get = copy.deepcopy(req)
                    data = req.cookies.copy()
                    data[cookie] = fuzz
                    req_get.update_cookies(data)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

                #Fuzz all headers
                headers = req.headers.copy()
                for head in headers.keys():
                    req_get = copy.deepcopy(req)
                    data = req.headers.copy()
                    data[head] = fuzz
                    req_get.update_headers(data)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

                #Fuzz url/?*fuzz*
                url = UrlObject(req.url)
                u = url.u_d + '?' + fuzz
                req_get = copy.deepcopy(req)
                req_get.update_url(u)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

                #Fuzz url/*fuzz*
                u = url.u_d + fuzz
                req_get = copy.deepcopy(req)
                req_get.update_url(u)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get) 
                    
            #====================================================
            #   Fuzz the same as before with URL encoded payloads
            #====================================================
                #Fuzz all GET and POST parameters a=*fuzz*, b=*fuzz* +encoded
                params = req.data.copy()
                for param in params.keys():
                    req_get = copy.deepcopy(req)
                    data = req.data.copy()
                    data[param] = fuzz_encoded
                    req_get.update_data(data)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

                #Fuzz all GET and POST parameters a=value*fuzz* +encoded
                for param in params.keys():
                    req_get = copy.deepcopy(req)
                    data = req.data.copy()
                    value = data[param]
                    data[param] = value + fuzz_encoded
                    req_get.update_data(data)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

                #Fuzz all cookies +encoded
                cookies = req.cookies.copy()
                for cookie in cookies.keys():
                    req_get = copy.deepcopy(req)
                    data = req.cookies.copy()
                    data[cookie] = fuzz_encoded
                    req_get.update_cookies(data)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

                #Fuzz all headers +encoded
                headers = req.headers.copy()
                for head in headers.keys():
                    req_get = copy.deepcopy(req)
                    data = req.headers.copy()
                    data[head] = fuzz_encoded
                    req_get.update_headers(data)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

                #Fuzz url/?*fuzz* +encoded
                url = UrlObject(req.url)
                u = url.u_d + '?' + fuzz_encoded
                req_get = copy.deepcopy(req)
                req_get.update_url(u)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

                #Fuzz url/*fuzz* +encoded
                u = url.u_d + fuzz_encoded
                req_get = copy.deepcopy(req)
                req_get.update_url(u)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

        return requestList
