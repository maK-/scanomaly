#This module is used to directory bust with a common directory list
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import random, copy

class Dirb(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        data = FileOp(rules['cwd']+'/lists/dirs.txt').reader()
        shuffled = random.shuffle(data) #Randomize our list
        newurl = ''
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
