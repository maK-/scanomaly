#This module is used to directory bust for filenames of specified filetypes
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys, copy

class DirbFiles(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects

        if rules['datalist'] == None:
            print('dirb-files: Provide a list of file extensions -dl html php')
            sys.exit(0)
        else:
            filetypes = rules['datalist']
            try:
                files = FileOp(rules['cwd']+'/lists/files.xtcz').reader()
            except:
                files = ['fail.xtcz']

            print('File Extensions: '+str(filetypes))
            for req in reqs:
                u = UrlObject(req.url)
                for ftype in filetypes:
                    for directory in files:
                        newurl = u.u_d + directory.replace('xtcz', ftype)
                        req_get = copy.deepcopy(req)
                        req_get.update_url(newurl)
                        req_get.update_reqID('reqID')
                        req_get.update_module(module)
                        requestList.append(req_get)
        return requestList
