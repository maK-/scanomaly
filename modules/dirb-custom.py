#This module is used to directory bust for a user provided list
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys, copy

class DirbCustom(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        try:
            custom_list = FileOp(rules['datalist'][0]).reader()
        except:
            print('dirb-custom: Provide a wordlist using -dl [wordlist]')
            sys.exit(0)
        for req in reqs:
            u = UrlObject(req.url)
            #For each item in custom list append to current url
            for directory in custom_list:
                newurl = u.u_d+directory
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)
        return requestList
