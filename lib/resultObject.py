#This object is used to represent the response data
#This data will usually be destined for a database

from colored import fg, bg, attr
class ResultObject:

    #Initialize our result object
    def __init__(self, respID, responseSize, statusCode, time, numHeaders, 
                    numTokens, headers, content):
        self.rs = attr('reset')
        self.respID = respID
        self.responseSize = responseSize
        self.statusCode = statusCode
        self.time = time
        self.numHeaders = numHeaders
        self.numTokens = numTokens
        self.headers = headers
        self.content = content

    #For debugging
    def printAll(self):
        #Print out all the data
        print(fg(4)+'response ID: '+ fg(2) + self.respID + self.rs)
        print(fg(4)+'size: '+ self.rs + self.responseSize)
        print(fg(4)+'status: '+ self.rs + self.statusCode)
        print(fg(4)+'time: '+ self.rs + self.time)
        print(fg(4)+'num_headers: '+ self.rs + self.numHeaders)
        print(fg(4)+'num_tokens: '+ self.rs + self.numTokens)
        print(fg(4)+'headers: '+self.rs+str(self.headers))
