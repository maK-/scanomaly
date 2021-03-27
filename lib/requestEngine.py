"""                            _   _____             _
 _ __ ___  __ _ _   _  ___ ___| |_| ____|_ __   __ _(_)_ __   ___
| '__/ _ \/ _` | | | |/ _ / __| __|  _| | '_ \ / _` | | '_ \ / _ \
| | |  __| (_| | |_| |  __\__ | |_| |___| | | | (_| | | | | |  __/
|_|  \___|\__, |\__,_|\___|___/\__|_____|_| |_|\__, |_|_| |_|\___|
             |_|                               |___/
*   Make lots of requests quickly and store interesting responses
*   Attempting to do smart things in a stupid way...
"""
from lib.resultObject import ResultObject
from lib.database import Database
from lib.notice import Notice
import multiprocessing as multi_p
from numpy import array_split
from colored import fg, bg, attr
import time
import apsw
import requests
import sys

#For Notice messaging
notice = Notice()

#A req object is generally referring to a request
class RequestEngine:
    """
    *   Initialize the RequestEngine object
    """
    def __init__(self, req_list, dbname, nthread, timeout, ig_size, ig_status,
                 same_flag, content_flag, session_flag, force_flag):
        self.rl = req_list.copy()               #full copy of requests
        self.request_list = []                  #For requests
        self.rl_size = len(req_list)            #total size of request list
        self.dbname = dbname                    #database to store to
        self.req_id = str(int(time.time()))     #used in naming and ID of reqs
        self.store_content = content_flag       #do we store full response?   
        self.session_flag = session_flag        #do we persist the req session?
        self.same_resp = same_flag              #is the endpoint a param brute?
        self.force = force_flag                 #do we continue after waf?
        self.timeout = timeout                  #timeout between each req?
        self.n_procs = nthread                  #number of concurrent procs   
        self.the_url = req_list[0].url
        
        #The database to store the results into
        if dbname != None:
            self.dbname = dbname
            self.resp_db = Database(dbname)
        else:
            self.dbname = None

        #Data to share between processes
        # - Make realtime decisions
        # - Track Progress
        # - Only store interesting results
        self.resp_q = multi_p.Queue()           #reqs to be stored
        self.scan_q = multi_p.Queue()           #reqs to be made
        self.manager = multi_p.Manager()        #create shared objects
        self.interest_reqs = self.manager.list() 
        self.interest_status = self.manager.list([200,302,301,500,401,403])
    
        #Clean end strategy to minimize deadlocks and avoid watcher queue     
        self.end_game = self.manager.list([x for x in range(0,self.n_procs)])
        self.end = self.manager.dict( {'count': 0} )

        #Lists of statuses and sizes to ignore
        self.ig_size = self.manager.list(list(map(int, ig_size)))
        self.ig_status = self.manager.list(list(map(int, ig_status)))
        
        #Keep track of last x amount of request (if all match, WAF kicked in)
        self.waf = self.manager.list([x for x in range(0,int(self.n_procs/2))])
        
        #Collect only the unique responses (based on size of) if same_resp set
        self.size_resp = { '200': self.manager.list(),
                           '301': self.manager.list(),
                           '302': self.manager.list(),
                           '401': self.manager.list(),
                           '403': self.manager.list(),
                           '500': self.manager.list(),
                           'other': self.manager.list() }
        #self.realtime = self.manager.dict(self.realtime_store)
        
        #Building the scan_q(ueue) of reqs and assigning request IDs to each
        for n in range(0, self.rl_size):
            req = req_list.pop(0)
            req.update_reqID(self.req_id+'@'+str(n))
            self.scan_q.put(req)
            self.request_list.append(req)
            notice.progress('Adding requests to queue: ', self.scan_q.qsize(),
                                self.rl_size)
        print('')
        notice.regs('Launching the application scanner...')
    

    """
    *   This function runs the tasks and manages multiple processes
    """
    def run(self):
        procs = [] #Store our multiple processes
        #Process to write responses to database
        p1 = multi_p.Process(target=self.response_to_db)
        procs.append(p1)
        #Add our specified number of procs and yolo the requests
        for i in range(0, self.n_procs):
            p = multi_p.Process(target=self.makereq, args=(i,self.session_flag))
            procs.append(p)
        try:
            for p in procs:
                p.start()
            for p in procs:
                p.join()
        except KeyboardInterrupt:
            notice.errs('Terminating processes...')
            for p in procs:
                p.terminate()
                sys.exit(0)
        procs = []

    """
    *   This function takes a request from the scan_q and makes it
    *   Responses are pushed to a resp_q to be added to the DB
    """
    def makereq(self, count, session_flag):
        response = None
        rq = requests.session()
        while not self.scan_q.empty():
            #Hack to stop running if all recent responses match
            if len(set(self.waf)) == 1 and self.force == False:
                break
            try:
                i = self.scan_q.get(timeout=10) #Raise empty exception after 10s
                response = i.request(rq, session_flag)
                
                if response != None:
                    if(int(response.responseSize) not in self.ig_size and
                        int(response.statusCode) not in self.ig_status):
   
                        #hack too stop running if a WAF kicks in
                        self.waf.append(response.statusCode)
                        self.waf.pop(0)
    
                        #If same_resp set, only store unique response sizes
                        #This is useful for fuzzing parameters
                        if self.same_resp == True:
                            other = False

                            #Use other if not in keys
                            if response.statusCode in self.size_resp.keys():
                                sizes = self.size_resp[response.statusCode]
                            else:
                                sizes = self.size_resp['other']
                                other = True
                          
                            #Has this size been seen before?        
                            if response.responseSize not in sizes:
                                if other == True:   #Is the status not in the list
                                    self.size_resp['other'].append(
                                        response.responseSize     )
                                    self.resp_q.put(response)
                                else:       #put the result into status key
                                    self.size_resp[response.statusCode].append(
                                        response.responseSize                 )
                                    self.resp_q.put(response)
                            else:
                                #has been seen before, add to ignore list
                                self.ig_size.append(int(response.responseSize))
                        else:
                            #store if unique
                            self.resp_q.put(response)
                        
                        #If force is set, add new WAF status to ignore
                        if len(set(self.waf)) == 1 and self.force == True:
                            self.ig_status.append(int(response.statusCode))
                            err = 'WAF Detected'+fg(1)+'! '+fg(4)
                            err += response.statusCode
                            notice.errs(err)
                time.sleep(self.timeout)
            except Exception:
                self.enders_game(count)
                return
        self.enders_game(count)
        return

    """
    *   This function takes a response off the resp_q and stores to DB
    """
    def response_to_db(self):
        time.sleep(5)
        count = 0
        while True:
            resp = self.resp_q.get()
            if resp == None:
                break
            else:
                if self.resp_db != None:
                    self.resp_db.insert_result(resp,self.store_content)
                    self.request_to_db(resp.respID) #Insert the request
                    count = self.resp_db.get_count()
                no_rq = self.rl_size - self.scan_q.qsize()
                progressupdate = 'Responses: '+fg(14)+str(count)+attr('reset')
                progressupdate += '\t\tPercentage Complete: '
                notice.progress(progressupdate,no_rq,self.rl_size)
        print('')
        #On completing, write our database from memory to a file
        if self.dbname != None:
            backupdb = apsw.Connection(self.dbname)
            notice.regs('Saving results to: '+fg(14)+self.dbname)
            with backupdb.backup("main", self.resp_db.conn, "main") as b:
                while not b.done:
                    b.step(100)
        #clean the remaining queue to avoid deadlock
        while not self.scan_q.empty():
            self.scan_q.get()
        return
    
    """
    *   This function matches the response to its req and stores req to DB 
    """
    def request_to_db(self, reqID):
        for i in self.rl:
            if reqID == i.reqID:
                self.resp_db.insert_request(i.get_requestObj())

    """
    *   This function increments our endgame counter
    """
    def enders_game(self, count):
        self.end_game.remove(count)
        if len(self.end_game) == 0:
            self.resp_q.put(None)
        
