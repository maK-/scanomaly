#This module attempts to bypass 403/401 directories
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import copy

class Bypass(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        common = []
        try:
            common = FileOp(rules['cwd']+'/lists/vhost-list.txt').reader()

            if len(rules['datalist']) > 1:
                domain = rules['datalist'][0]
                domains = FileOp(rules['datalist'][1]).reader()
            elif len(rules['datalist']) == 1:
                domains = FileOp(rules['datalist'][0]).reader()
        except:
            print('vhost module: -dl [domain] [subs.txt] or -dl [subs.txt]')
        
        if len(rules['datalist']) > 1:
            for req in reqs:
                for dom in common:
                    req_get = copy.deepcopy(req)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    head_get = req.headers.copy()
                    head_get['Host']=dom
                    req_get.update_headers(head_get)
                    requestList.append(req_get)

                    req_get = copy.deepcopy(req)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    head_get = req.headers.copy()
                    head_get['Host']=dom+'.'+domain
                    req_get.update_headers(head_get)
                    requestList.append(req_get)

                    req_get = copy.deepcopy(req)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    head_get = req.headers.copy()
                    head_get['Host']=dom+'-'+domain
                    req_get.update_headers(head_get)
                    requestList.append(req_get)
            
        if len(domains) > 0:
            for req in reqs:
                for dom in domains:
                    req_get = copy.deepcopy(req)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    head_get = req.headers.copy()
                    head_get['Host']=dom
                    req_get.update_headers(head_get)
                    requestList.append(req_get)

        return requestList
