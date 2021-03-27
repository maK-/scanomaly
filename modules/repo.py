#This module is used to directory bust with repo, config and meta-data files
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import random, copy

class Repo(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        data = FileOp(rules['cwd']+'/lists/files.txt').reader()
        shuffled = random.shuffle(data) #Randomize our list
        newurl = ''
        for req in reqs:
            u = UrlObject(req.url)
            for repo in data:
                newurl = u.u_d+repo
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)
        return requestList
