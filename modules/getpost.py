#This module gets request baselines
#=========================
from yapsy.IPlugin import IPlugin          
from lib.requestObject import RequestObject
from lib.urlObject import UrlObject
from lib.fileOp import FileOp
import random
import string

class GetPost(IPlugin):

    def __init__(self):
        self.requestList = []

    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module):

        for url in urls:
            u = UrlObject(url)

            #Standard GET request
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, u.full, postdata, module)
            self.requestList.append(req_get)

            #POST request with params in postdata
            pdata = u.query
            req_post = RequestObject('reqID', 'POST', proxy, headers, timeout,
                                        cookies, u.u_q, pdata, module)
            self.requestList.append(req_post)
        
        return self.requestList
