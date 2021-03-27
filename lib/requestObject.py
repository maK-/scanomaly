"""                            _    ___  _     _           _
 _ __ ___  __ _ _   _  ___ ___| |_ / _ \| |__ (_) ___  ___| |_
| '__/ _ \/ _` | | | |/ _ / __| __| | | | '_ \| |/ _ \/ __| __|
| | |  __| (_| | |_| |  __\__ | |_| |_| | |_) | |  __| (__| |_
|_|  \___|\__, |\__,_|\___|___/\__|\___/|_.___/ |\___|\___|\__|
             |_|                            |__/
*   It stores the various properties of a request. It does the following:
*           - Read requests from a file                   (parse())
*           - Output a full request to a file
*           - Print a full request
*           - Print the request/response combination with filters
*           - Update or set any unique part of a request  (update_*())  
*           - return a request object for database import (get_requestObj())
*           - Rebuild a request object using same format as requestObj
*           - Make a request then store a responseObject  (request())
"""
import requests
import time
import urllib3
import sys
import json
from re import findall
from lib.resultObject import ResultObject
from lib.urlObject import UrlObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from http.server import BaseHTTPRequestHandler
from io import BytesIO
from copy import copy

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#This class is to extend a request handler
class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

# This is our main Request Object
class RequestObject:
    def __init__(self, url):
        if url == 'http' or url == 'https':
            self.url = url+'://'
        else:
            self.url = url
        self.data = {}
        self.headers = {}
        self.cookies = {}
        self.timeout = 5
        self.method = ''
        self.proxy = ''
        self.module = ''
        self.reqID = 'reqID'
        
        #Booleans
        self.is_JSON = False    #Is the request JSON 
        self.is_DATA = False    #Is the request a POST or PARAM data

    #Import a raw HTTP request from a file into the object
    def parse(self, filename):
        data = FileOp(filename).reader_s()
        databytes = bytearray()
        databytes.extend(data.encode())
        parsed_req = HTTPRequest(databytes)

        #If no error parsing then populate the object with data from file
        if(parsed_req.error_code == None):
            #========================
            #Parse headers and method
            #========================
            self.headers = dict(parsed_req.headers)
            self.method = parsed_req.command
            #==================
            #Parse request body
            #==================
            try:
                content_len = int(self.headers['Content-Length'])
            except:
                content_len = 0
                pass
            if content_len > 0:
                self.data = str(parsed_req.rfile.read(content_len).decode())
                self.data = ParseArguments().parseData(self.data)
            else:
                self.data = {}
            #===========================
            #Parse full url from request
            #===========================
            try:
                host = self.headers['Host']
            except:
                host = ''
                pass
            self.url = self.url + host
            if self.url.endswith('/') == False:
                self.url = self.url + parsed_req.path
            #===================================
            #Parse Cookies from provided headers
            #===================================
            try:
                cookiestr = self.headers['Cookie']
                del self.headers['Cookie']
                self.cookies = ParseArguments.parseCookies(cookiestr)
            except:
                self.cookies = {}
                pass

    #Update request ID
    def update_reqID(self, upd_reqID):
        try:
            self.reqID = copy(upd_reqID)
        except Exception as e:
            print('upd reqID')
            print(e)

    #Update the module for request
    def update_module(self, upd_mod):
        try:
            self.module = copy(upd_mod) 
        except Exception as e:
            print('upd module')
            print(e)

    #Update Proxy
    def update_proxy(self, upd_proxy):
        try:
            self.proxy = copy(dict(upd_proxy))
        except Exception as e:
            print('upd proxy')
            self.proxy = {}
            print(e)

    #Update method
    def update_method(self, upd_method):
        try:
            self.method = copy(upd_method)
        except Exception as e:
            print('upd method')
            print(e)

    #Update url
    def update_url(self, upd_url):
        try:
            self.url = copy(upd_url)
        except Exception as e:
            print('upd url')
            print(e)

    #Update cookies
    def update_cookies(self, upd_cookies):
        try: 
            cookies = copy(upd_cookies)
            self.cookies.update(cookies)
        except Exception as e:
            print('upd cookies')
            print(e)

    #Update headers
    def update_headers(self, upd_headers):
        try:
            headers = copy(upd_headers)
            self.headers.update(headers)
        except Exception as e:
            print('upd headers')
            print(e)

    #Update data
    def update_data(self, upd_data):
        try:
            data = copy(upd_data)
            self.data.update(data)
        except Exception as e:
            print('upd data')
            print(e)

    #Update data value
    def update_values(self, key, upd_val):
        try:
            self.data[key] = upd_val
        except Exception as e:
            print('upd values')
            print(e)

    #Get request object data for DB
    def get_requestObj(self):
        self.req_data = {
                            "reqID": str(self.reqID),
                            "method": str(self.method),
                            "proxy": str(dict(self.proxy)),
                            "headers": str(json.dumps(dict(self.headers))),
                            "cookies": str(json.dumps(dict(self.cookies))),
                            "url": str(self.url),
                            "data": str(json.dumps(dict(self.data))),
                            "module": str(self.module)
                        }
        return self.req_data

    #Set from db requestObj
    def set_requestObj(self, req_data):
        try:
            self.update_reqID(req_data['reqID'])
            self.update_method(req_data['method'])
            self.update_proxy(req_data['proxy'])
            self.update_headers(req_data['headers'])
            self.update_cookies(req_data['cookies'])
            self.update_url(req_data['url'])
            self.update_data(req_data['data'])
            self.update_module(req_data['module'])
            return True
        except Exception as e:
            print('>>> set_requestObj')
            print(e)
            return False

    #Make a request using provided session
    def request(self, session, session_flag):
        try:
            self.startTime = time.time()
            if(session_flag):
                r = session
            else:
                r = requests
            rq = ''
            resp_data = {
                            "respID": str(self.reqID),
                            "responseSize": str(-1),
                            "statusCode": str(-1),
                            "time": str(-1),
                            "numHeaders": str(-1),
                            "numTokens": str(-1),
                            "headers": str(-1),
                            "content": str(-1)
            }

            #Is the request JSON based?
            if 'Content-type' in self.headers.keys():
                if 'application/json' in self.headers['Content-type']:
                    self.is_JSON = True

            #Is the requests sending data via POST?
            POSTY = ['POST','PUT','PATCH']
            if self.method in POSTY:
                self.is_DATA = True
        except Exception as e:
            print('Error before request')
            print(e)

        try:
            #==============================================================
            #   This is where requests are made so debugging here is useful
            #==============================================================
            if self.is_DATA == True:
                if self.is_JSON == True:
                    rq = r.request(self.method, self.url, timeout=self.timeout,
                                    verify=False, allow_redirects=False,
                                    headers=self.headers, cookies=self.cookies,
                                    proxies=self.proxy, json=self.data)
                else:
                    rq = r.request(self.method, self.url, timeout=self.timeout,
                                    verify=False, allow_redirects=False,
                                    headers=self.headers, cookies=self.cookies,
                                    proxies=self.proxy, data=self.data)
                
            else:
                rq = r.request(self.method, self.url, timeout=self.timeout,
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                proxies=self.proxy, params=self.data)

            resp_data = {
                            "respID": str(self.reqID),
                            "responseSize": str(len(rq.content)),
                            "statusCode": str(rq.status_code),
                            "time": str((time.time() - self.startTime)),
                            "numHeaders": str(len(rq.headers)),
                            "numTokens": str(len(findall(r'\w+', rq.text))),
                            "headers": str(json.dumps(dict(rq.headers))),
                            "content": str(rq.text)
            }
        except requests.exceptions.Timeout:
            resp_data['statusCode'] = '-1'
            pass
        except requests.exceptions.ConnectTimeout:
            resp_data['statusCode'] = '-2'
            pass
        except requests.exceptions.ConnectionError:
            resp_data['statusCode'] = '-3'
            pass
        except requests.exceptions.TooManyRedirects:
            resp_data['statusCode'] = '-4'
            pass
        except Exception as e:
            print(e)
            
        #Create a response Object
        self.responseObj = ResultObject(resp_data['respID'], 
                                        resp_data['responseSize'],
                                        resp_data['statusCode'],
                                        resp_data['time'], 
                                        resp_data['numHeaders'],
                                        resp_data['numTokens'],
                                        resp_data['headers'],
                                        resp_data['content'])
        return self.responseObj

    def printAll(self):
        if self.url != None:
            url = UrlObject(self.url)
            path = url.fullpath
            host = url.host
            headrs = dict(self.headers)
            print('\nRequest ID:'+self.reqID)
            print('Module: '+self.module)
            print(self.method+' '+str(path)+' HTTP/1.1')
            print('Host: '+host)
            for k,v in headrs.items():
                print(k+': '+v)
            print('-------------------------------')
            print(self.cookies)
            print(self.data)
            print(self.url)
