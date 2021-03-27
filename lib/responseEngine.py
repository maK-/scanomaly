"""                                      _____             _
 _ __ ___ ___ _ __   ___  _ __  ___  ___| ____|_ __   __ _(_)_ __   ___
| '__/ _ / __| '_ \ / _ \| '_ \/ __|/ _ |  _| | '_ \ / _` | | '_ \ / _ \
| | |  __\__ | |_) | (_) | | | \__ |  __| |___| | | | (_| | | | | |  __/
|_|  \___|___| .__/ \___/|_| |_|___/\___|_____|_| |_|\__, |_|_| |_|\___|
             |_|                                     |___/
*   This class aims to capture anomalies in responses
*       - Returns a list of requests objects for further processing
*       - Eventually we can import "post" modules to handle individual module
          parsing (will allow more complex follow ups)
"""
from lib.requestObject import RequestObject
from lib.urlObject import UrlObject
from lib.notice import Notice
from yapsy.PluginManager import PluginManager

import copy

notice = Notice()
class ResponseEngine:
    def __init__(self, db, main_config, cwd):
        self.db = db
        self.cnf = main_config

        #The output needs to have the statuses/sizes to ignore and the relevant
        #modules and baseline request
        self.b_cnf = {  "i_status": [],
                        "i_size": [],
                        "mods": [],
                        "flagsame": False,
                        "session": False,
                        "force": False,
                        "timeout": 0,                      
        }
        
        self.multi_Req = []
        self.statuses = []
        self.responses = {}
        self.requests = {}
        self.module = ''    #use the baseline_parse else standard_parse if not


        #Process post plugin modules
        manager = PluginManager()
        manager.setPluginPlaces([cwd+"/modules/post"])
        manager.collectPlugins()
        self.all_plugins= manager.getAllPlugins()
        
    """
    *   Parse out the responses into a list of lists per status
    """
    def parse_db(self):
        self.statuses = self.db.get_statuses()
        self.responses = self.db.get_responses_by_status(self.statuses)
        

        #when no unique results in responses DB
        if len(self.statuses) == 0:
            notice.errs('No entries in database to parse!')
            return False
        #Parse out diff requests by status
        for k,v in self.responses.items():
            for resp in v:
                request = self.db.get_request_by_id(resp['respID'])
                req_object = RequestObject(None)
                fucking_proxy = copy.deepcopy(request)
                fucking_proxy['proxy'] = {}
                req_object.set_requestObj(fucking_proxy)
                if k in self.requests.keys():
                    self.requests[k].append(copy.deepcopy(req_object))
                else:
                    self.requests[k] = [copy.deepcopy(req_object)]
        
        #Get the current db module type
        self.module = self.get_module_name()
        
        #Print the responses by status code
        self.print_responses()
        return True


    """
    *   Do plugin based parsing here and return remaining for default
    """
    def baseline_parse(self):
            self.standard_parse()

    """
    *   This section parses normal anomaly responses and generates requests
    """
    def standard_parse(self):
        for k,v in self.responses.items():
            for req in v:
                u = copy.deepcopy(self.get_request(req['respID']))
                url = UrlObject(u.url)
                if k == '200':
                    if url.is_dir():
                        self.b_cnf = self.cnf._200_d
                        self.b_cnf['url'] = copy.copy(url.full)
                        self.b_cnf['req'] = copy.deepcopy(
                                                self.get_request(req['respID']))
                        self.multi_Req.append(copy.deepcopy(self.b_cnf))
                    elif url.is_compatable():
                        self.b_cnf = self.cnf._200_e
                        self.b_cnf['url'] = copy.copy(url.full)
                        self.b_cnf['req'] = copy.deepcopy(
                                                self.get_request(req['respID']))
                        self.multi_Req.append(copy.deepcopy(self.b_cnf))
                elif k == '403':
                    self.b_cnf = self.cnf._403
                    self.b_cnf['url'] = copy.copy(url.full)
                    self.b_cnf['req'] = copy.deepcopy(
                                            self.get_request(req['respID']))
                    self.multi_Req.append(copy.deepcopy(self.b_cnf))
                elif k == '401':
                    self.b_cnf = self.cnf._401
                    self.b_cnf['url'] = copy.copy(url.full)
                    self.b_cnf['req'] = copy.deepcopy(
                                            self.get_request(req['respID']))
                    self.multi_Req.append(copy.deepcopy(self.b_cnf))
                elif k == '301':
                    self.b_cnf = self.cnf._301
                    self.b_cnf['url'] = copy.copy(req['headers']['Location'])
                    request = copy.deepcopy(self.get_request(req['respID']))
                    request.update_url(copy.copy(req['headers']['Location']))
                    self.b_cnf['req'] = request
                    self.multi_Req.append(copy.deepcopy(self.b_cnf))
        return True


    #check if first 3 responses match
    def matching_3(self):
        mini_list = []
        for k,v in self.responses.items():
            if len(v) == 3:
                for i in v:
                    mini_list.append(i['statusCode'])

        if set(mini_list) == 1:
            return True
        else:
            return False

    #check if all match (add size to ignore list)
    def all_match(self):
        mini_list = []
        for k,v in self.responses.items():
            if len(v) == 6:
                for i in v:
                    mini_list.append(i['statusCode'])
        if set(mini_list) == 1:
            return True
        else:
            return False

    def all_sizes_match(self):
        mini_list = []
        for k,v in self.responses.items():
            if len(v) == 6:
                for i in v:
                    mini_list.append(i['responseSize'])
        if set(mini_list) == 1:
            return mini_list[0]
        else:
            return False
                

    #Used for strict baseline parsing
    def strip_respID(self, respID):
        resp_id = {"id": respID.split('@')[0],
                   "req": respID.split('@')[1]}
        return resp_id

    #Is the current database a baseline?
    def is_baseline(self):
        if self.module == 'baseline':
            return True
        else:
            return False

    #is the b_cnf empty
    def is_bcnf_empty(self):
        empty = True
        if len(self.b_cnf['mods']) != 0:
            empty = False
        if len(self.b_cnf['i_status']) != 0:
            empty = False
        return empty

    #return the base request @0
    def get_base(self):
        for k,v in self.responses.items():
            for i in v:
                resp_id = i['respID']
                resp = self.strip_respID(resp_id)
                if resp['req'] == '0':
                    for req in self.requests[k]:
                        if req.reqID == resp_id:
                            return req

    #return the request matching the respID
    def get_request(self, respID):
        for k,v in self.requests.items():
            for i in v:
                if respID == i.reqID:
                    return i

    #get count of number of responses
    def get_count(self):
        counter = 0
        for v in self.requests.values():
            for i in v:
                count += 1
        return counter


    #Print counts
    def print_responses(self):
        for k,v in self.responses.items():
            notice.infos(str(k)+': '+str(len(v)))
            
    #Return the module name
    def get_module_name(self):
        status = str(self.statuses[0])
        req = self.requests[status][0]
        module = req.module     
        return module
