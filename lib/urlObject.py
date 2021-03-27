import string
from urllib.parse import urlparse

''' _   _      _  ___  _     _           _
   | | | |_ __| |/ _ \| |__ (_) ___  ___| |_
   | | | | '__| | | | | '_ \| |/ _ \/ __| __|
   | |_| | |  | | |_| | |_) | |  __| (__| |_
    \___/|_|  |_|\___/|_.___/ |\___|\___|\__|
                          |__/
Url Object for easier parsing ( http://x.com/demo/test.html?x=1 )
====================================================
u.orig = original url passed into parser
u.u_d = current url to last dir (http://x.com/demo/)
u.u_dd = current url -1 dir (function)
u.u_q = current url without query string (http://x.com/demo/test.html)
u.full = full url (http://x.com/demo/test.html?x=1)
u.fullpath = path (/demo/test.html?x=1)
u.host = network location (x.com)
u.query = full query (x=1)
u.lastpath = name of last directory (demo)
u.lastfile = last file (test.html)
u.lastfile_ext = last file without extension (test)
u.last_ext = file extension (html)
u.lenpath = number of paths in url (demo/test.html = 2)
'''
class UrlObject:
    def __init__(self, url):
        self.orig = url
        self.u = urlparse(url)
        self.u_q = self.u[0]+'://'+self.u[1]+self.u[2]
        self.full = self.u.geturl()
        self.query = self.u[4]
        self.fullpath = self.u.path
        self.host = self.u.netloc
        self.lastpath = ''
        self.lastfile = ''
        self.lastfile_ext = ''
        self.last_ext = ''
        self.lenpath = 0
        self.u_d = ''
        self.u_dd = ''
        self.base = self.u.scheme+'://'+self.host+'/'

        #Useful vars
        if '/' in self.u[2]:
            self.path = self.u[2].split('/')
            self.lenpath = len(self.path)-1

        #==============
        #   Get u_d
        #==============
        if self.lenpath > 1:
            if self.is_compatable()==True and '/' in self.u[2]:
                tmp_u_d = self.u[2].split('/')
                self.lastfile = tmp_u_d.pop()
                tmp_u_d.pop(0)
                self.u_d = self.base+'/'.join(tmp_u_d)+'/'
                self.lastpath = tmp_u_d.pop()
            elif self.is_compatable()==False and '/' in self.u[2]:
                tmp_u_d = self.u[2].split('/')
                self.lastfile = tmp_u_d.pop()
                tmp_u_d.pop(0)
                self.u_d = self.base+'/'.join(tmp_u_d)+'/'
                self.lastpath = tmp_u_d.pop()
            else:
                self.u_d = self.base
                self.lastfile = self.u[2].split('/').pop(1)
            if self.u_d.endswith('//'):
                self.u_d = self.u_d[:-1]
        else:
            self.u_d = self.base
            self.lastpath = ''
            self.lastfile = self.u[2].split('/').pop(1)

        #===============
        #   Get u_dd 
        #===============
        if self.lenpath > 2:
            if self.lastpath != '':
                tmp_u_dd = self.u[2].split('/')
                tmp_u_dd.pop(0)
                tmp_u_dd.pop()
                tmp_u_dd.pop()
                self.u_dd = self.base+'/'.join(tmp_u_d)+'/'
            else:
                self.u_dd = self.base
        else:
            self.u_dd = self.base 

        #================================
        #   Get lastfile/extensions etc
        #================================
        if '.' in self.lastfile:
            tmp_lastfile = self.lastfile.split('.')
            self.last_ext = tmp_lastfile.pop()
            if len(tmp_lastfile) > 1:
                self.lastfile_ext = '.'.join(tmp_lastfile)
            elif len(tmp_lastfile) == 0:
                self.lastfile_ext = ''
            else:
                self.lastfile_ext = tmp_lastfile.pop(0)
        
    #Determine if the url is a directory or an endpoint
    def is_endpoint(self):
        if len(self.lastfile) == 0:
            return True
        else:
            return False

    #Parameter brute forcing compatable extension?
    def is_compatable(self):
        extensions = [  'php','php3','php4','php5','phtml','pl','py',
                        'jsp','jsf','action','jspx','jhtml','do','wss',
                        'asp','aspx','axd','asx','asmx','svc','esp',
                        'wsdl','cfm','cgi','dll','rb','rhtml'
                     ]
        if self.last_ext in extensions:
            return True
        else:
            return False

    #Check if url is a dir
    def is_dir(self):
        if (len(self.lastfile) == 0 and len(self.query) == 0 and  
                self.full.endswith('/')):
            return True
        else:
            return False
