"""                  _       _      _____             _
 _ __ ___   ___   __| |_   _| | ___| ____|_ __   __ _(_)_ __   ___
| '_ ` _ \ / _ \ / _` | | | | |/ _ |  _| | '_ \ / _` | | '_ \ / _ \
| | | | | | (_) | (_| | |_| | |  __| |___| | | | (_| | | | | |  __/
|_| |_| |_|\___/ \__,_|\__,_|_|\___|_____|_| |_|\__, |_|_| |_|\___|
                                                |___/
*   This takes lists of requestObjects and modules to run
*       - The specified modules can be loaded on any request object
*       - It returns a list of requests ready for the requestEngine
"""
from lib.notice import Notice
from colored import fg
notice = Notice()
class ModuleEngine:
    def __init__(self, multi_req, mods_to_run, rules):
        self.multi_reqs = multi_req.copy()
        self.mods = mods_to_run
        #The rules object can hold the following:
        #   - cwd
        #   - datalist
        self.rules = rules
        
        #Return total requests so we can keep overall tally
        self.total_count = 0

        #Full list of modded requests for requestEngine
        self.multi_Req = []
    
        #Attempted fix for DB names including module
        self.multi_Wreck = {}   #dbname:[reqs]

        #run modules over multi_req
        temp_results = []               #temporary store of results for each
        for url, req_list in self.multi_reqs.items():
            notice.infos('Target: '+fg(2)+url)
            mod_count = 0             #per module count
            for module in self.mods:
                notice.infos('Module: '+fg(2)+module.name)
                temp_results = module.plugin_object.gen( req_list, module.name,
                                                         self.rules )
                notice.infos('Imported: '+fg(2)+str(len(temp_results)))
                self.multi_Wreck[module.name] = temp_results
                self.multi_Req.append(temp_results)
                mod_count += len(temp_results)
            self.total_count += mod_count
            notice.regs('Requests for Target: '+fg(14)+str(mod_count))
            mod_count = 0
            notice.splits()
        #notice.errs('Total Requests: '+fg(1)+str(total_count))
                 


