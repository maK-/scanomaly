#This module implements scanning for the content discovery techniques of the kiterunner tool
#reference: https://github.com/assetnote/kiterunner
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import random, copy

class KiteRunnerPOC(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        data2 = FileOp(rules['cwd']+'/lists/kiterunner-routes-small.txt').reader()
        
        #Use some different contexts
        api_context = ['1','-1','0','33e2c9de-991a-11eb-a8b3-0242ac130003','064ad4e2-31a1-4559-8d96-83d17feca4e4','00000000-0000-0000-0000-000000000000','1.0','%00','NULL']
        
        #Build URL lists
        data = []
        for c in api_context:
            for route in data2:
                if route.startswith('/'):
                    route = route[1:]
                newpath = route.replace('{kr}',c)
                data.append(newpath)

        for req in reqs:
            u = UrlObject(req.url)
            for directory in data:
                newurl = u.u_d+directory
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)
        return requestList
