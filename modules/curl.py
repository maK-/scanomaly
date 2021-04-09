#This module runs specified requests, handy for discovery
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import copy

class Curl(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        for req in reqs:
            req_get = copy.deepcopy(req)
            req_get.update_reqID('reqID')
            req_get.update_module(module)
            requestList.append(req_get)
        return requestList
