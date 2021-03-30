#This module is used to directory bust for a user provided dir or file
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys, copy

class DirbSingle(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        
        if rules['datalist'] == 0:
            print('dirb-single: -dl Provide directories or files to scan for')
            sys.exit(0)
        else:
            for req in reqs:
                u = UrlObject(req.url)
                #For each item in data list append to current url
                for directory in rules['datalist']:
                    newurl = u.u_d+directory
                    req_get = copy.deepcopy(req)
                    req_get.update_url(newurl)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)
        return requestList
