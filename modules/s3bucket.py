#This module is used to scan for s3buckets
#Use 1 for old style aws URL & 2 for new style
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import random

class S3Bucket(IPlugin):
    def gen(self, cwd, urls, proxy, headers, timeout, cookies, 
            postdata, module, dataList):
        requestList = []    #Store generated request objects
        tempList = set()
        data = FileOp(cwd+'/lists/buckets.txt').reader()
        data = data + dataList
        separators = ['.','-','_']
        shuffled = random.shuffle(data) #Randomize our list
        s3url = 'https://s3.amazonaws.com/'
        bucketurl = '.s3.amazonaws.com/'
        
        #Add permutations of data for larger list
        #for i in data:
        #    tempList.add(i)
        #    for j in data:
        #        tempList.add(i+j)
        #        tempList.add(j+i)
        #        for k in separators:
        #            tempList.add(i+k+j)
        #            tempList.add(j+k+i)

        #Generate custom buckets using dataList
        tempdata = []
        for i in dataList:
            for j in data:
                tempdata.append(i+j)
                tempdata.append(j+i)
                for k in separators:
                    tempdata.append(i+k+j)
                    tempdata.append(j+k+i)

        #Generate the s3 URLS to scan
        s3urls = []
        for i in tempdata:
            if "1" in urls:
                s3urls.append(s3url + i + '/')
            if "2" in urls:
                s3urls.append('https://'+ i + bucketurl)

        #Create request object list from urls
        for url in s3urls:        
            req_get = RequestObject('reqID','GET', proxy, headers, timeout,
                                        cookies, url, postdata, module)
            requestList.append(req_get)
        return requestList
