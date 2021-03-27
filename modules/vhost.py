#This module is used to scan for vhosts
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import sys
import random

class Vhost(IPlugin):
    def gen(self, cwd, urls, proxy, headers, timeout, cookies,
            postdata, module, datalist):
        requestList = []
        domain = ''
        domains = []
        common = FileOp(cwd+'/lists/vhost-list.txt').reader()
        try:
            if len(datalist) > 1:
                domain = datalist[0]
                domains = FileOp(datalist[1]).reader()
            elif len(datalist) == 1:
                domain = datalist[0]
        except:
            print('vhost module: -dl [domain] [list of subdomains] ')
            sys.exit(0)
            
        for url in urls:
            for i in common:
                new_h = headers.copy()
                new_h['Host'] = i
                req_get = RequestObject('reqID', "GET", proxy, new_h, timeout, 
                                        cookies, url, postdata, module)
                requestList.append(req_get)

                new_h = headers.copy()
                new_h['Host'] = i+'-'+domain
                req_get = RequestObject('reqID', "GET", proxy, new_h,
                                         timeout, cookies, url,
                                         postdata, module)
                requestList.append(req_get)
                if i != '':
                    subd = i+'.'+domain
                    new_h = headers.copy()
                    new_h['Host'] = subd
                    req_get = RequestObject('reqID', "GET", proxy, new_h, 
                                            timeout, cookies, url, postdata, 
                                            module)
                    requestList.append(req_get)


            if len(datalist) > 1:
                for i in domains:
                    new_h = headers.copy()
                    new_h['Host'] = i
                    req_get = RequestObject('reqID', "GET", proxy, new_h, 
                                            timeout, cookies, url, postdata,
                                            module)
                    requestList.append(req_get)
        return requestList
