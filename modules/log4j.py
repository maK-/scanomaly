#This module is used to fuzz all request parameters
#With user provided payloads
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import copy
import sys

class Fuzz(IPlugin):
    def getParamStr(self, reqdata):
        dataString = ''
        if len(reqdata) != 0:
            for i,j in reqdata.items():
                dataString += i + '=' + j
                dataString += '&'
        return dataString[:-1]

    def gen(self, reqs, module, rules):
        requestList = []   #Store generated request objects
        params = FileOp(rules['cwd']+'/lists/parameters.txt').reader()
        headers = FileOp(rules['cwd']+'/lists/all-headers.txt').reader() 

        if len(rules['datalist']) == 0:
            print('fuzz: -dl [fuzz payload] [fuzz payload] ...')
            sys.exit(0)

        for fuzz in rules['datalist']:
            paramValue = fuzz
            headerValue = fuzz
            db = ''
            
            #Add custom fuzz to path
            for req in reqs:
                u = UrlObject(req.url)
                newurl = u.u_d+paramValue
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

            #Add custom fuzz to path+?
            for req in reqs:
                u = UrlObject(req.url)
                newurl = u.u_d+'?'+paramValue
                req_get = copy.deepcopy(req)
                req_get.update_url(newurl)
                req_get.update_reqID('reqID')
                req_get.update_module(module)
                requestList.append(req_get)

            #Included headers coverage (like user agent etc)
            for req in reqs:
                req_head = copy.deepcopy(req)
                heads = req.headers.copy()
                newhead = copy.deepcopy(heads)
                for h,value in heads.items():
                    req_head2 = copy.deepcopy(req)
                    newhead[h] = headerValue           
                    req_head2.update_headers(heads)                               
                    req_head2.update_reqID('reqID')                               
                    req_head2.update_module(module)                               
                    requestList.append(req_head2)                                 
                    del newhead[h]

        
            mini_headers = [ 'X-Api-Version','User-Agent','Cookie','Referer',
                        'Accept-Language','Accept-Encoding',
                        'Upgrade-Insecure-Requests','Accept','Pragma',
                        'X-Requested-With','X-CSRF-Token','Dnt',
                        'Content-Length','Access-Control-Request-Method',
                        'Access-Control-Request-Headers','Warning',
                        'Authorization','TE','Accept-Charset','Accept-Datetime',
                        'Expect','Forwarded','From','Max-Forwards',
                        'Proxy-Authorization', 'X-Forwarded-For', 'Range',
                        'Content-Deposition', 'X-Amz-Target','Content-Type',
                        'Username','IP', 'IPaddress','Hostname']
            #Generate requests using mini_headers and value provided
            for req in reqs:
                req_head = copy.deepcopy(req)
                heads = req.headers.copy()
                for h in mini_headers:
                    newheaders = copy.deepcopy(heads)
                    newheaders[h] = headerValue
                    req_new = copy.deepcopy(req_head)
                    req_new.update_headers(newheaders)
                    req_new.update_reqID('reqID')
                    req_new.update_module(module)
                    requestList.append(req_new)
                    
        return requestList
