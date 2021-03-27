"""
* The goal of a module is to generate requests to be carried out,       *
* There are multiple libraries available to make this process easier.   *
* Many arguments are passed from the command line. The goal is rapid    *
* creation, prototyping weaponizing of proof of concept fuzzing ideas!  *
*                                                                       *
* `-dl` This allows strings to be passed to modules via the CLI         *
*       Strings could be filenames to import or general input for your  *
*       for your module to leverage. The datalist parameter is a list.  *
*                                                                       *
* A module returns a list of RequestObjects that are requests to be made*
"""
#This is an example module to demonstrate how requests can be manipulated
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject

class Example(IPlugin):

    #Generate our requests
    def gen(self, reqs, module, rules):
        """
        * reqs is the CLI provided list of requests or baseline request*
        * these are the requestObjects a module manipulates.           *
        """
        requestList = []   #Store generated requests to be made
       
        module_input = rules['datalist']            
        if len(module_input) == 0:
            print('Example: Use -dl [your instructions]')

        """
        * The following are a list of mutable request fields           *
        * Each can be called like .headers, .cookies to return values  *
        * from request objects.                                        *
        """

        """request.update_module(string)"""
        #Update the module name
        
        """request.update_proxy(string)"""
        #Update the request proxy

        """request.update_method(string)"""
        #Update the request method (GET POST etc)

        """request.update_url(string)"""
        #Update the request path/url/where the request goes

        """request.update_cookies(string)"""
        #Update the cookie values

        """request.update_headers(string)"""
        #Update the request headers

        """request.update_data(string)"""
        #Update the request data (POST/JSON parameters etc)

        """request.update_values(key, value)"""
        #Update the value of a parameter

        
        
        
        for request in reqs:
            new_request = copy.deepcopy(request)
                    heads = req.headers.copy()
                    heads['Authorization'] = data
                    req_head.update_headers(heads)
                    req_head.update_reqID('reqID')
                    req_head.update_module(module)
                    requestList.append(req_head)
                    del heads[head]
        return requestList
