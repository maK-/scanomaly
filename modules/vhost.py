#This module attempts to bypass 403/401 directories
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import copy

class Vhost(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        common = []
        domains = []
        try:
            common = FileOp(rules['cwd']+'/lists/vhost-list.txt').reader()

            if len(rules['datalist']) > 1:
                domain = rules['datalist'][0]
                domains = FileOp(rules['datalist'][1]).reader()
            elif len(rules['datalist']) == 1:
                domains = FileOp(rules['datalist'][0]).reader()
            else:
                domains = []
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

        #Add a bypass scan too for common proxy headers
        local_range = ['127.0.0.1', '10.0.0.1', '172.16.0.1', '192.168.0.1','127.1']
        headers = ['X-Originating-IP','X-Forwarded-For','X-Remote-IP',
                   'X-Remote-Addr','X-Forwarded-Host','X-Host','X-Remote-Addr',
                   'X-Client-IP','X-Real-IP','True-Client-IP',
                   'CF-Connecting-IP', 'X-Cluster-Client-IP',
                   'Fastly-Client-IP']

        #Check each header with each IP
        for ip in local_range:
            for head in headers:
                for dom in domains:
                    req_head = copy.deepcopy(req)
                    req_head.update_reqID('reqID')
                    req_head.update_module(module)
                    heads = req.headers.copy()
                    heads['Host']=dom
                    heads[head] = ip
                    req_head.update_headers(heads)
                    requestList.append(req_head)
                    del heads[head]
        
        #Add the same with referrer headers
        headers = ['Referer']
        for ip in local_range:
            for head in headers:
                for dom in domains:
                    req_head = copy.deepcopy(req)
                    req_head.update_reqID('reqID')
                    req_head.update_module(module)
                    heads['Host']=dom
                    heads[head] = 'http://'+ip+'/hax'
                    req_head.update_headers(heads)
                    requestList.append(req_head)
                    del heads[head]
        return requestList
