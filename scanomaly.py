#!/usr/bin/env python3
"""
                                           _
 ___  ___ __ _ _ __   ___  _ __ ___   __ _| |_   _
/ __|/ __/ _` | '_ \ / _ \| '_ ` _ \ / _` | | | | |
\__ | (_| (_| | | | | (_) | | | | | | (_| | | |_| |
|___/\___\__,_|_| |_|\___/|_| |_| |_|\__,_|_|\__, |
                                             |___/
*   This tool is a web application fuzzer
*       - It takes requests, a url or list of urls
*       - Modifies the requests using different pluggable modules
*       - Modified requests are made and the responses are collected
*       - The goal being to identify security issues or anomalies in responses
*       - modules: ANYTHING - fuzzing, discovery, brute force etc.
*   Keep it short, simple, extendable and sexy
"""
import sys, argparse, time, os, copy, uuid
from lib.requestObject import RequestObject
from lib.agentObject import UserAgent
from lib.requestEngine import RequestEngine
from lib.moduleEngine import ModuleEngine
from lib.responseEngine import ResponseEngine
from lib.version import VersionInfo
from lib.notice import Notice
from lib.dataparser import ParseArguments
from lib.configparser import ConfigParser
from lib.fileOp import FileOp
from lib.database import Database
from lib.anomalyDetect import AnomalyDetect
from lib.mergeDB import MergeDBs
from lib.meiliSearching import MeiliS
from yapsy.PluginManager import PluginManager
from colored import fg, bg, attr

rs = attr('reset')
notice = Notice()
if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-a', '--agent', type=str, default='Scanomaly v2.0',
                        help=fg(8)+'Specify a user agent'+rs)
    parse.add_argument('-ai', '--anomaly', action='store_true', default=False,
                        help=fg(8)+'do anomaly on db entries'+rs)
    parse.add_argument('-al', '--agentlist', action='store_true', default=False,
                        help=fg(8)+'random agent from list for all requests'+rs)
    parse.add_argument('-ar', '--agentran', action='store_true', default=False,
                        help=fg(8)+'randomise agent for every request'+rs)
    parse.add_argument('-aM', '--allmethod',action='store_true',default=False,
                        help=fg(8)+'use all common methods!'+rs)
    parse.add_argument('-c', '--cookie', type=str, default=None,
                        help=fg(8)+'specify cookie string'+rs)
    parse.add_argument('-cwd', '--setdir', type=str, default=None,
                        help=fg(8)+'set current working dir manually'+rs)
    parse.add_argument('-cfg', '--config', type=str, default=None,
                        help=fg(8)+'specify path to config directory'+rs)
    parse.add_argument('-d', '--data', type=str, default=None,
                        help=fg(8)+'specify data like a=b&c=d (GET params)'+rs)
    parse.add_argument('-dl', '--datalist', nargs='+',
                        help=fg(8)+'pass list of args to modules'+rs)
    parse.add_argument('-db', '--database', type=str, default=None,
                        help=fg(8)+'specify a database to use'+rs)
    parse.add_argument('-f', '--force', action='store_true', default=False,
                        help=fg(8)+'force continuation if WAF kicks in'+rs)
    parse.add_argument('-fs', '--flagsame', action='store_true', default=False,
                        help=fg(8)+'ignore non unique sizes'+rs)
    parse.add_argument('-H', '--headers', nargs='+',
                        help=fg(8)+'add headers in format "a:b" "c:d"'+rs)
    parse.add_argument('-ic', '--content', action='store_true', default=False,
                        help=fg(8)+'store full response content in DB'+rs)
    parse.add_argument('-l', '--listmods', action='store_true', default=False,
                        help=fg(8)+'list all modules and info'+rs)
    parse.add_argument('-m', '--modules', nargs='+',
                        help=fg(8)+'specify modules to load and use'+rs)
    parse.add_argument('-mi', '--modinfo', action='store_true', default=False,
                        help=fg(8)+'print module information'+rs)
    parse.add_argument('-M', '--methods', nargs='+', default=['GET'],
                        help=fg(8)+'specify methods to use'+rs)
    parse.add_argument('-mei', '--meilisearch', nargs='+', default=[],
                        help=fg(8)+'Dump to meilisearch'+rs)
    parse.add_argument('-conn', '--meiconn', nargs='+', default=[]
                        help=fg(8)+'Meilisearch connect <ip> <port> <passw>'+rs)
    parse.add_argument('-p', '--proxy', type=str, default=None,
                        help=fg(8)+'Use a proxy (http|s://[ip]:[port])'+rs)
    parse.add_argument('-P', '--printed', action='store_true', default=False,
                        help=fg(8)+'Print all results at end'+rs)
    parse.add_argument('-P2', '--printresp', action='store_true', default=False,
                        help=fg(8)+'Print all results and response content'+rs)
    parse.add_argument('-r', '--request', type=str, default=None,
                        help=fg(8)+'specify a request file to import'+rs)
    parse.add_argument('-s', '--isize', nargs='+', default=[],
                        help=fg(8)+'Ignore response of size (26 12345 350)'+rs)
    parse.add_argument('-sf', '--session', action='store_false', default=True,
                        help=fg(8)+'Do not use persistent server session'+rs)
    parse.add_argument('-scan', '--scans', action='store_true', default=False,
                        help=fg(8)+'run a single scan using modules'+rs)
    parse.add_argument('-SCAN', '--scanner', action='store_true', default=False,
                        help=fg(8)+'run beast mode scanning using config :)'+rs)
    parse.add_argument('-t', '--threads', type=int, default=2,
                        help=fg(8)+'specify number of threads to use'+rs)
    parse.add_argument('-tt', '--requestTimeout', type=int, default=0,
                        help=fg(8)+'seconds to wait between each request'+rs)
    parse.add_argument('-T', '--timeout', type=int, default=10,
                        help=fg(8)+'seconds to wait for response'+rs)
    parse.add_argument('-u', '--url', type=str, default=None,
                        help=fg(8)+'Specify a URL to use'+rs)
    parse.add_argument('-ul', '--urlist', type=str, default=None,
                        help=fg(8)+'Specify a list of URLs'+rs)
    parse.add_argument('-v', '--version', action='store_true', default=True,
                        help=fg(8)+'display version information'+rs)
    parse.add_argument('-x', '--istatus',nargs='+',default=[404,400,405,501],
                        help=fg(8)+'specify status to ignore (eg 503 400)'+rs)
    """
    parse.add_argument('-test','--testdecision', action='store_true', 
                        default=False, help=fg(8)+'Test decision functions'+rs)
    parse.add_argument('-db2', '--dbase2', type=str, default=None,
                        help=fg(8)+'Database for diff functionality'+rs)
    parse.add_argument('-diff', '--diffdbs', type=int, default=0,
                        help=fg(8)+'Diffs between dbs (Use -db and -db2)'+rs)
    """
    args = parse.parse_args()

    #Request variables
    all_methods = [ "GET", "POST", "OPTIONS", "PUT", "PATCH", "HEAD",
                    "DELETE", "TRACE", "DEBUG", "AAA" ]
    total_headers = {}
    cookies = {}
    proxies = {}
    data = {}
    timeout = args.timeout
    total_headers.update({'User-Agent':args.agent})

    #List of urls to scan
    urlList = []

    #Multi url dictionary of request lists
    multi_url = {}

    #List of request objects to process
    ReqList = []

    #List of multi url requests objects to process
    multi_Req = []

    #Current working directory
    cwd = os.getcwd()  
    if args.setdir != None:
        cwd = args.setdir

    #Process plugin modules
    manager = PluginManager()
    manager.setPluginPlaces([cwd+"/modules"])
    manager.collectPlugins()
    all_plugins= manager.getAllPlugins()

    #If there's no arguments, display help
    if len(sys.argv) <= 1:
        version = VersionInfo(cwd)
        version.show()
        parse.print_help()
        sys.exit(0)

    #Display version info
    if args.version == True:
        version = VersionInfo(cwd)
        version.show()

    #Import request from file and sort URL
    if args.request != None and args.url != None:
        req = RequestObject(args.url)
        req.parse(args.request)
    
    #Create request object if only url provided
    if args.request == None and args.url != None:
        req = RequestObject(args.url)

    #Add user supplied headers
    if args.headers != None:
        headers = ParseArguments().parseHeaders(args.headers)
        for i in headers:
            total_headers.update({i:headers[i]})

    #Add user supplied cookies
    if args.cookie != None:
        cookies = ParseArguments().parseCookies(args.cookie)

    #Add user supplied proxy
    if args.proxy != None:
        proxies = ParseArguments().parseProxy(args.proxy)

    #Add user supplied request body data
    if args.data != None:
        datas = ParseArguments().parseData(args.data)
        if len(datas) > 0:
            for i in datas:
                data.update({i:datas[i]})
        else:
            data = ''
    
    #Update request object, add to urlList
    if args.url != None:
        urlList = []
        req.update_headers(total_headers)
        req.update_proxy(proxies)
        req.update_cookies(cookies)
        req.update_data(data)
        if args.allmethod:
            for method in all_methods:
                newreq = copy.deepcopy(req)
                newreq.update_method(method)
                urlList.append(newreq)
        else:
            for method in args.methods:
                newreq = copy.deepcopy(req)
                newreq.update_method(method)
                urlList.append(newreq)
        multi_url[urlList[0].url] = urlList

    #Generate a list of urls
    if args.urlist != None:
        urlist = FileOp(args.urlist).reader()
        if len(multi_url) == 0:
            for url in urlist:
                urlMulti = []
                req = RequestObject(url)
                req.update_headers(total_headers)
                req.update_proxy(proxies)
                req.update_cookies(cookies)
                req.update_data(data)
                if args.allmethod:
                    for method in all_methods:
                        newreq = copy.deepcopy(req)
                        newreq.update_method(method)
                        urlMulti.append(newreq)
                else:
                    for method in args.methods:
                        newreq = copy.deepcopy(req)
                        newreq.update_method(method)
                        urlMulti.append(newreq)
                multi_url[url] = urlMulti
        #If multi_url already exists
        else:
            multi_temp = {}
            for urln, req_list in multi_url.items():
                for requ in req_list:
                    req_temp = copy.deepcopy(requ)
                    for url in urlist:
                        urlMulti = []
                        data_temp = ParseArguments().parseUrlData(url)
                        req_temp.update_data(data_temp)
                        req_temp.update_url(url)
                        urlMulti.append(req_temp)
                        multi_temp[url] = urlMulti
                multi_url = multi_temp
       
    for multi in multi_url.values():
        for requ in multi:
            temp_url = requ.url
            if '?' in temp_url:
                temp_url = temp_url.split('?')[0]
            temp_url += ParseArguments().parseUrlfromData(data)
            requ.update_url(temp_url)
    
    #The following code handles the loading and running of modules
    if args.modules != None:
        all_mods = []   
        mods_to_run = []
        
        #Get all plugins + add user supplied modules to list that are valid
        for plugin in all_plugins:
            all_mods.append(plugin.name)
        for module in args.modules:
            if module in all_mods:
                mod_object = manager.getPluginByName(module)     
                mods_to_run.append(mod_object)

        if(args.modinfo):
            notice.infos(fg(2)+'==== Module Information ====')
            notice.splits()
            for module in mods_to_run:
                notice.infos('Name: '+fg(2)+module.name)
                notice.infos('Description: '+fg(8)+module.description)
                notice.infos('Author: '+fg(8)+module.author)
                notice.infos('Website: '+fg(8)+module.website)
                notice.splits()
        
        #useful info for modules
        mod_rules = { 'cwd': cwd,
                      'datalist': args.datalist
        }
        mod_engine = ModuleEngine(multi_url, mods_to_run, mod_rules)
        multi_Wreck = mod_engine.multi_Wreck
        total_requests = mod_engine.total_count
        
    elif args.modules == None and args.scans == True:
        notice.errs('No modules loaded: '+fg(1)+'use -m flag')
        sys.exit(0)
                    
    #Change all requests in list to random agent
    if args.agentlist == True and ReqList != None:
        ua = UserAgent(ReqList, cwd)
        ReqList = ua.agentlist()

    #Change all requests to random agents
    if args.agentran == True and ReqList != None:
        ua = UserAgent(ReqList, cwd)
        ReqList = ua.agentran()

    #List all modules and associated info
    if args.listmods == True:
        notice.infos(fg(2)+'==== Module Information ====')
        notice.splits()
        for mod in all_plugins:
            notice.infos('Name: '+fg(2)+mod.name)
            notice.infos('Description: '+fg(8)+mod.description)
            notice.infos('Author: '+fg(8)+mod.author)
            notice.infos('Website: '+fg(8)+mod.website)
            notice.splits()

    """
    *       - Run a basic bitch manual scan like other tools
    """
    if args.scans == True:
        db_tmp_dir = cwd+'/'+'tmp/'+str(uuid.uuid1())+'/'
        try:
            os.mkdir(db_tmp_dir)
        except OSError:
            notice.errs('Could not create directory: '+fg(1)+db_tmp_dir)
            sys.exit(0)
        
        #List to store database runs
        db_lists = []
        
        for modname,reqList in multi_Wreck.items():
            ts = int(time.time())
            db_name = db_tmp_dir+args.database+modname+str(ts)+'.db'
            db_lists.append(db_name)
            r_engine = RequestEngine(reqList, db_name, args.threads, 
                                        args.requestTimeout, args.isize, 
                                        args.istatus, args.flagsame,
                                        args.content, args.session, args.force)
            r_engine.run()
        
        #Merge all module databases into one                                     
        output_database = cwd+'dbs/'+args.database+'.db'                             
        merge = MergeDBs(db_lists, output_database)                              
        merge.processList()                                                      
        notice.infos('Databases merged: '+fg(2)+output_database)                 
                                                                                 
        #Testing storage 
        outdb = Database(output_database)                                       
        outdb.return_all(args.istatus, args.isize)

        if len(args.meilisearch) > 0:
            meilidata = MeiliS(outdb.return_data(), args.database, 
                               args.meiconn, args.meilisearch)
            meilidata.import_all()

    if args.scanner == False and args.scans == False:
        if len(args.meilisearch) > 0:
            outdb = Database(args.database)
            meilidata = MeiliS(outdb.return_data(), args.database, 
                               args.meiconn, args.meilisearch)
            meilidata.import_all()
    


    """                                           _
    *     ___  ___ __ _ _ __   ___  _ __ ___   __ _| |_   _
    *    / __|/ __/ _` | '_ \ / _ \| '_ ` _ \ / _` | | | | |
    *    \__ | (_| (_| | | | | (_) | | | | | | (_| | | |_| |
    *    |___/\___\__,_|_| |_|\___/|_| |_| |_|\__,_|_|\__, |
    *                                                 |___/
    *    The real stupid shit starts here.
    *   ----------------------------------------------------
    *       - Parse all the configs
    *       - Scan -> Collect Responses -> Run through mods -> Repeat
    """
    if args.scanner == True:
        #======================
        #   Parsing the configs
        #======================
        config = ConfigParser(cwd, 'config/')
        conf = config.config
        
        #=============================================================
        #   Create a new directory for all the scan result dbs to live
        #=============================================================
        db_tmp_dir = cwd+'/'+'tmp/'+str(uuid.uuid1())+'/'
        try:
            os.mkdir(db_tmp_dir)
        except OSError:
            notice.errs('Could not create directory: '+fg(1)+db_tmp_dir)
            sys.exit(0)

        #Store some shit!
        db_lists = []               #Store most recent dbs completed to Parse
        unique_urls = {}            #[args.url]=[list of dbs] unique urls hit!
        unique_urls[args.url] = []  #Skip the first url
        rules = {   'cwd': cwd,     #For Module generator
                    'datalist': args.datalist
        }
        req_multi = {}              #For formatting into ModuleEngine
        

        #===================================================
        #   Start the scanner using cli and default options!
        #===================================================
        for modname,reqList in multi_Wreck.items():
            ts = int(time.time())
            db_name = db_tmp_dir+args.database+modname+str(ts)+'.db'
            db_lists.append(db_name)
            unique_urls[args.url].append(db_name)
            r_engine = RequestEngine(reqList, db_name, args.threads,
                                        conf['timeout'], conf['i_size'],
                                        conf['i_status'], conf['flagsame'],
                                        conf['content'], conf['session'],
                                        conf['force'])
            r_engine.run()
            new_db_list = []    #replaces db_lists after each full run
        #======================================================
        #   Start our recursion depth loop for scanning results
        #======================================================
        for x in range(0, int(conf['recursion_depth'])):
            for db in db_lists:
                print(db_lists)

                #Parse responses from completed database, generate new scans
                outdb = Database(db)
                resp_engine = ResponseEngine(outdb, config, cwd)
                resp_engine.parse_db()
                resp_engine.baseline_parse()
    
                #For each new unique request config generated by ResponseEngine
                for r_cnf in resp_engine.multi_Req:
                    if r_cnf['url'] not in unique_urls.keys():
                        unique_urls[r_cnf['url']] = []
                    else:
                        continue
                    
                    #==================================================
                    #   Get module objects from confg to run on request
                    #==================================================
                    all_mods = []
                    mods_to_run = []
                    for plugin in all_plugins:
                        all_mods.append(plugin.name)
                    for mod in r_cnf['mods']:
                        if module in all_mods:
                            mod_object = manager.getPluginByName(mod)
                            mods_to_run.append(mod_object)
                    
                    #Replicate old multi request format (like when using CLI)
                    key = r_cnf['url']
                    req_multi[key] =  [r_cnf['req']]
                    
                    #======================================
                    #   Do some gangster assed fuzzing shit
                    #======================================
                    mod_engine = ModuleEngine(req_multi, mods_to_run, rules)
                    multi_Req = mod_engine.multi_Wreck                  
                    total_requests += mod_engine.total_count
                    notice.errs('Total Requests: '+fg(1)+str(total_requests))
                    req_multi = {}
                    for modname,reqList in multi_Req.items():
                        ts = int(time.time())
                        db_name = db_tmp_dir + args.database + modname
                        db_name += str(ts)+'.db'
                        new_db_list.append(db_name)
                        unique_urls[r_cnf['url']].append(db_name)
                        r_e = RequestEngine(reqList, db_name, args.threads,
                                            r_cnf['timeout'],r_cnf['i_size'],
                                            r_cnf['i_status'],r_cnf['flagsame'],
                                            r_cnf['content'],r_cnf['session'],
                                            r_cnf['force'] )
                        r_e.run()
            db_list = copy.copy(new_db_list)
            new_db_list = []

        
        #write a list of urls covered to a text file in the directory
        store_urls = FileOp(db_tmp_dir+'urls.txt').writer(unique_urls.keys())
        
        #Print out all results 
        for url,db in unique_urls.items():
            notice.regs('Target: '+fg(14)+url)
            for i in db:
                outdb = Database(i)
                outdb.return_all(args.istatus, args.isize)
                

        #Maybe all results should be merged into one database here?
        #Trying Meilisearch
                                                
    #Print output from DB
    if args.printed == True and args.database != None:
        outdb = Database(args.database)
        outdb.return_all(args.istatus, args.isize)

    #Print output from DB including responses
    if args.printresp == True and args.database != None:
        outdb = Database(args.database)
        outdb.return_detail(args.istatus, args.isize)

    """
    #Print AI output from DB
    if args.anomaly == True and args.database != None:
        outdb = Database(args.database)
        find_anomalies = outdb.ai_parse()
        results = AnomalyDetect(find_anomalies)
        results.getByStatus()

    #Diff databases 
    if args.diffdbs != 0 and args.database != None and args.dbase2 != None:
        notice.infos('Diffs: ')
        notice.regs('Database 1: '+fg(2)+args.database)
        notice.regs('Database 2: '+fg(2)+args.dbase2)
        baseline = Database(args.database)
        diffs = Database(args.dbase2)
        data2 = diffs.return_data()
        baseline.return_diffs(data2, args.diffdbs)
    elif args.diffdbs == 0 and args.dbase2 != None:
        notice.errs('Error! Provide a verbosity level: -diff [1-3]')
        notice.infos('1 - Show only diffs')
        notice.infos('2 - Show original baseline and diffs')
        notice.infos('3 - Show all')


    if args.database != None and args.testdecision == True:
        print('ready to decide?')
        baseline = Database(args.database)
        #read all response data from database
        testbed = baseline.get_data()
        #function to parse data
    """
