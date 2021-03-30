#This module is used to scan for s3buckets
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import copy, sys

class S3Bucket(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []    #Store generated request objects
        
        url = '.s3.amazonaws.com/'
        separators = ['.','-','_']

        if rules['datalist'] == None:
            print('s3bucket module: -dl [companyname] [related words]...')
            sys.exit(0)
        else:           
            data = FileOp(rules['cwd']+'/lists/buckets.txt').reader()
            data = data + rules['datalist']
            tempdata = []
            for a in rules['datalist']:
                for b in data:
                    tempdata.append(a+b)
                    tempdata.append(b+a)
                    for c in separators:
                        tempdata.append(a+c+b)
                        tempdata.append(b+c+a)
            tempdata = set(tempdata)
            for req in reqs:
                for permutation in tempdata:
                    req_get = copy.deepcopy(req)
                    req_get.update_url('https://'+permutation+url)
                    req_get.update_reqID('reqID')
                    req_get.update_module(module)
                    requestList.append(req_get)
        return requestList
