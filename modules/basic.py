#This module is used to brute force basic auth
#Use -dl [username] [password list]
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys, base64

class Basic(IPlugin):
    def gen(self, reqs, module, rules):
        requestList = []   #Store generated request objects
       
        usernames = rules['datalist']            
        if len(usernames) == 0:
            print('basic: Use -dl [usernames]')
        passwords = FileOp(rules['cwd']+'/lists/password.txt').reader()
        common = ['root', 'admin', 'test', 'demo', 'dev']
        users = set(common + usernames)
        
        
        for req in reqs:
            for user in users:
                for passwd in passwords:
                    data = user+':'+passwd
                    auth = base64.b64encode(data.encode())
                    data = 'Basic '+auth.decode()
                    req_head = copy.deepcopy(req)
                    heads = req.headers.copy()
                    heads['Authorization'] = data
                    req_head.update_headers(heads)
                    req_head.update_reqID('reqID')
                    req_head.update_module(module)
                    requestList.append(req_head)
                    del heads[head]
        return requestList
