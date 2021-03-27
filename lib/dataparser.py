#This class parses headers, data etc.
from colored import fg, bg, attr
import json

class ParseArguments:
    def  __init__(self):
        self.rs = attr('reset')
        self.new = {}

    #Handle the parsing of CLI user supplied headers
    def parseHeaders(self, headers):
        for i in headers:
            try:
                key = i.split(':')[0]
                value = i.split(':')[1]
                self.new[key.strip()] = value.strip()
            except IndexError:
                print(fg(1)+'Wrong header format detected: '+self.rs+str(i))
                continue
        return self.new

    #Handle the parsing of user supplied cookies
    def parseCookies(self, cookie):
        try:
            cookies = cookie.split(';')
            for i in cookies:
                if len(i) != 0:
                    try:
                        key = i.split('=')[0]
                        value = i.split('=')[1]
                        self.new.update({key.strip():value.strip()})
                    except IndexError:
                        print(fg(1)+'Cookie Error: '+self.rs+str(i))
                        continue
        except IndexError:
                print(fg(1)+'Cookies Error: '+self.rs+str(cookie))
        return self.new

    #Handle the parsing of a user supplied proxy
    def parseProxy(self, proxy):
        if 'https://' in proxy:
            self.new['https'] = proxy.split('https://')[1]
        elif 'http://' in proxy:
            self.new['http'] = proxy.split('http://')[1]
        else:
            print(fg(1)+'Incorrect Proxy Format: '+self.rs+str(proxy))
        return self.new
            
    #Handle data parsing
    def parseData(self, data):
        print('before:' + str(data))
        json_data = self.parseJSON(data)
        print(json_data)
        if json_data == False:
            datas = []
            if '=' in data:
                try:
                    datas = data.split('&')
                    for i in datas:
                        key = i.split('=')[0]
                        value = i.split('=')[1]
                        self.new.update({key:value})
                    return self.new
                except IndexError:
                    key = data.split('=')[0]
                    value = data.split('=')[1]
                    self.new.update({key:value})
                    return self.new
        else:
            self.new = json_data
            return self.new

    #Handle if request body is Json
    def parseJSON(self, data):
        dict_data = {}
        try:
            datas = json.loads(str(data))
            dict_data = dict(datas)
        except:
            return False
        return dict_data

    #Handle data parsing from URL
    def parseUrlData(self, url):
        if '?' in url:
            data = url.split('?')[1]
            self.new = self.parseData(data)
        return self.new

    #Convert data back to URL
    def parseUrlfromData(self, data):
        urlstring='?'
        for i in data:
            urlstring += i + '=' + data[i] + '&'
        return urlstring[:-1]
            
