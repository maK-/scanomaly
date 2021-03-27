#This module gets request baselines
#=========================
from yapsy.IPlugin import IPlugin          
from lib.requestObject import RequestObject
from lib.urlObject import UrlObject
from lib.fileOp import FileOp
import random
import string
import copy

class Baseline(IPlugin):

    def __init__(self):
        self.strings = string.ascii_uppercase
        self.strings += string.ascii_lowercase
        self.strings += string.digits
        self.tenstr = ''.join(random.choices(self.strings, k=10))
        self.hundredstr = ''.join(random.choices(self.strings, k=100))

    def gen(self, reqs, module, rules):
        requestList = []   #Store generated request objects

        """
        *   The baseline request will later be used for smarter things
        *   For example auto ignoring status codes or certain sizes
        *   or a baseline to detect anomalies or deviations.
        """
        for req in reqs:
            #Standard baseline request                              0
            req_0 = copy.deepcopy(req)
            req_0.update_module(module)
            requestList.append(req_0)

            #Does our response size change for each request?        1
            req_1 = copy.deepcopy(req)
            req_1.update_module(module)
            requestList.append(req_1)

            #Does a random parameter change the response size       2
            req_2 = copy.deepcopy(req)
            req_2.update_module(module)
            data = copy.copy(req.data)
            data[self.tenstr] = self.hundredstr
            req_2.update_data(data)
            requestList.append(req_2)
            """            
            #Does the response change if the content-type is Json   3
            req_3 = copy.deepcopy(req)
            req_3.update_module(module)
            headr = {'Content-type': 'application/json'}
            req_3.update_headers(headr)
            requestList.append(req_3)

            #Does the response change if the content-type is XML    4
            req_4 = copy.deepcopy(req)
            req_4.update_module(module)
            headr = {'Content-type': 'text/xml'}
            req_4.update_headers(headr)
            requestList.append(req_4)
            """
            #Baseline of a 404 dir                                  5
            req_5 = copy.deepcopy(req)
            req_5.update_url(req_5.url + self.tenstr)
            req_5.update_module(module)
            requestList.append(req_5)

            #Different for a file?                                  6
            req_6 = copy.deepcopy(req)
            req_6.update_url(req_6.url + self.tenstr + '.html')
            req_6.update_module(module)
            requestList.append(req_6)

            #Baseline of large 404 (is url reflected in body?)      7
            req_7 = copy.deepcopy(req)
            req_7.update_url(req_7.url + self.hundredstr)
            req_7.update_module(module)
            requestList.append(req_7)
            """
            #Baseline of OPTIONS request                            8+
            req_get = copy.deepcopy(req)
            req_get.update_module(module)
            req_get.update_method("OPTIONS")
            requestList.append(req_get)
            """

        return requestList
