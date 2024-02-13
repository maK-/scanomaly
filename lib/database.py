#This class is used to store response objects
import apsw
from lib.resultObject import ResultObject
from colored import fg, bg, attr
import json
class Database:
    #Initialize the database
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = apsw.Connection(':memory:')
        self.cursor = self.conn.cursor()
        self.rs = attr('reset')

        #Create Response tables
        create = 'CREATE TABLE IF NOT EXISTS responses('
        create += 'timestamp datetime default current_timestamp,'
        create += 'respID text NOT NULL,'
        create += 'responseSize text NOT NULL,'
        create += 'statusCode text NOT NULL,'
        create += 'time text NOT NULL,'
        create += 'numHeaders text NOT NULL,'
        create += 'numTokens text NOT NULL,'
        create += 'headers text NOT NULL,'
        create += 'content text)'
        self.cursor.execute(create)

        #Create Requests tables
        create = 'CREATE TABLE IF NOT EXISTS requests('
        create += 'reqID text NOT NULL,'
        create += 'method text NOT NULL,'
        create += 'proxy text NOT NULL,'
        create += 'headers text NOT NULL,'
        create += 'cookies text NOT NULL,'
        create += 'url text NOT NULL,'
        create += 'data text NOT NULL,'
        create += 'module text NOT NULL)'
        self.cursor.execute(create)
    
    #Insert response Object into database
    def insert_result(self, resObj, storecontent):
        data = {
                    "respID": str(resObj.respID),
                    "responseSize": str(resObj.responseSize),
                    "statusCode": str(resObj.statusCode),
                    "time": str(resObj.time),
                    "numHeaders": str(resObj.numHeaders),
                    "numTokens": str(resObj.numTokens),
                    "headers": str(resObj.headers),
                    "content": str(resObj.content)
                }
        if not storecontent:
            data['content'] = ''
        insert = 'INSERT INTO responses(respID,responseSize,statusCode,time,'
        insert += 'numHeaders,numTokens,headers,content) VALUES (:respID,'
        insert += ':responseSize,:statusCode,:time,:numHeaders,:numTokens,'
        insert += ':headers,:content)'
        try:
            self.cursor.execute(insert, data)
        except Exception as e:
            print('SQL Error: insert_result')
            print(e)

    #Insert request Object
    def insert_request(self, reqObj):
        insert = 'INSERT INTO requests(reqID,method,proxy,headers,cookies,'
        insert += 'url,data,module) VALUES (:reqID,:method,:proxy,:headers,'
        insert += ':cookies,:url,:data,:module)'
        try:
            self.cursor.execute(insert, reqObj)
        except Exception as e:
            print('SQL Error: insert request')
            print(e)

    #Get number of entries
    def get_count(self):
        select = 'SELECT COUNT(*) FROM responses'
        try:
            self.cursor.execute(select)
            results = self.cursor.fetchone()
            return results[0]
        except Exception as e:
            print('SQL Error: get_count')
            print(e)
            pass

    #Get response IDs
    def get_responses(self):
        respdata = []
        select = 'SELECT respID FROM responses'
        try:
            self.cursor.execute(select)
            resps = self.cursor.fetchall()
            for i in resps:
                respdata.append(i[0])
            return respdata
        except Exception as e:
            print('SQL Error: get responses')
            print(e)

    #Print all out
    def return_all(self, i_status, i_size):
        resps = self.return_data()
        try:
            forprint = fg(1)+'Module: '+fg(12)+'Method '+self.rs+'URL '
            forprint += fg(10)+'status '+fg(15)+'size '+fg(3)+'time '
            forprint += fg(13)+'numHeaders '+fg(14)+'numTokens '+fg(8)+'reqID'
            forprint += self.rs
            print(forprint)
            for i in resps:
                response = fg(1)+i[0]+self.rs+': '+fg(12)+i[8]+' '+self.rs+i[1]
                response += ' '+fg(10)+i[4]+' '+fg(15)+i[3]+' '+fg(3)+i[5]+' '
                response += fg(13)+i[6]+' '+fg(14)+i[7]+'  '+fg(8)+i[11]
                response += self.rs
                if i[4] not in i_status:
                    if i[3] not in i_size:    
                        print(response)
        except Exception as e:
            print(e)
        return

    #Print all and response
    def return_detail(self, i_status, i_size):
        resps = self.return_data()
        try:
            forprint = fg(1)+'Module: '+self.rs+'URL '+fg(10)+'status '+fg(15)
            forprint += 'size '+fg(3)+'time '+fg(13)+'numHeaders '+fg(14)
            forprint += 'numTokens'+fg(8)+' headers'+self.rs
            print(forprint)
            for i in resps:
                response = fg(1)+i[0]+self.rs+': '+self.rs+i[1]+' '
                response += fg(10)+i[4]+' '+fg(15)+i[3]+' '+fg(3)+i[5]+' '
                response += fg(13)+i[6]+' '+fg(14)+i[7]+'  '+fg(8)+i[10]
                response += self.rs
                if i[4] not in i_status:
                    if i[3] not in i_size:
                        print(response)
                        print(i[9])
     
        except Exception as e:
            print(e)
        return

    #Return all without printing
    def return_data(self):
        self.conn = apsw.Connection(self.dbfile)
        self.cursor = self.conn.cursor()
        select = 'SELECT requests.module,requests.url,requests.headers,'
        select += 'responses.responseSize,responses.statusCode,responses.time,'
        select += 'responses.numHeaders,responses.numTokens,requests.method, '
        select += 'responses.content,responses.headers,requests.reqID FROM '
        select += 'requests INNER JOIN responses ON '
        select += 'responses.respID == requests.reqID'
        try:
            self.cursor.execute(select)
            datas = self.cursor.fetchall()
        except Exception as e:
            print(e)
            datas = []
        return datas

    #Select all status codes from database
    def get_statuses(self):
        statuses = []
        self.conn = apsw.Connection(self.dbfile)
        self.cursor = self.conn.cursor()
        select = 'SELECT statusCode from responses GROUP BY (statusCode)'
        try:
            self.cursor.execute(select)
            data = self.cursor.fetchall()
        except Exception as e:
            print(e)
            return statuses
        for i in data:
            statuses.append(i[0])
        return statuses

    """
    *   This selects responses from the database ordered by the most frequent
    *   of each statusCode. This means we can possibly minimize duplicates later
    *   Example: blah.com/server-status && blah.com/server-status/uebubefu
    *            We should only scan the first as anything after server-status
    *            will also be a 403. Minimize the things we scan a bit.         
    """
    def get_responses_by_status(self, statuses):
        responses = {}
        templates = ['200','302','301','500','401','403']
        other_results = []
        self.conn = apsw.Connection(self.dbfile)
        self.cursor = self.conn.cursor()
        for i in statuses:
            temp_results = []
            data = { 'statusCode': str(i) }
            select = 'SELECT *,totals.counts from responses LEFT JOIN '
            select += '(SELECT responseSize,COUNT(responseSize) as counts FROM'
            select += ' responses GROUP BY responseSize) totals on '
            select += 'responses.responseSize = totals.responseSize WHERE '
            select += 'statusCode = :statusCode ORDER by totals.counts DESC'
            try:
                self.cursor.execute(select, data)
                response = self.cursor.fetchall()
                for resp in response:
                    the_data = {}
                    the_data['timestamp'] = resp[0]
                    the_data['respID'] = resp[1]
                    the_data['responseSize'] = resp[2]
                    the_data['statusCode'] = resp[3]
                    the_data['time'] = resp[4]
                    the_data['numHeaders'] = resp[5]
                    the_data['numTokens'] = resp[6]
                    the_data['headers'] = dict(json.loads(resp[7]))
                    the_data['content'] = resp[8]
                    if i not in templates:
                        other_results.append(the_data)
                    else:
                        temp_results.append(the_data)
                if i in templates:
                    responses[i] = temp_results
            except Exception as e:
                print(e)
        if len(other_results) != 0:
            responses['others'] = other_results
        return responses

    #Select request object using response ID
    def get_request_by_id(self, respID):
        self.conn = apsw.Connection(self.dbfile)
        self.cursor = self.conn.cursor()
        data = { 'reqID': respID }
        select = 'SELECT * from requests where reqID = :reqID'
        try:
            self.cursor.execute(select, data)
            req = self.cursor.fetchone()
            the_data = {}
            the_data['reqID'] = req[0]
            the_data['method'] = req[1]
            the_data['proxy'] = req[2]
            the_data['headers'] = dict(json.loads(req[3]))
            the_data['cookies'] = dict(json.loads(req[4]))
            the_data['url'] = req[5]
            the_data['data'] = dict(json.loads(req[6]))
            the_data['module'] = req[7]
        except Exception as e:
            print(e)
        return the_data
        
        
    #Diff data between two datbase outputs
    def return_diffs(self, secondlist, verbosity):
        firstlist = self.return_data()
        print1 = fg(1)+'Method: '+self.rs+'URL '+fg(4)+'status '+fg(10)
        print1 += 'size '+fg(13)+'numHeaders '+fg(14)+'numTokens'+self.rs
        print(print1+'\n')
        for i in firstlist:
            method = i[8]
            url = i[1]
            size = i[3]
            status = i[4]
            numH = i[6]
            numT = i[7]
            if verbosity == 2 or verbosity == 3:
                print2 = fg(1)+method+self.rs+': '+url+' '+fg(4)+status+' '
                print2 += fg(10)+size+' '+fg(13)+numH+' '+fg(14)+numT+self.rs
                print(print2)
            for j in secondlist:
                if url in j[1] and method == j[8]:
                    if (size != j[3] or status != j[4] or 
                        numH != j[6] or numT != j[7]):
                        print3 = fg(2)+j[8]+': '+j[1]+' '+j[4]+' '+j[3]
                        print3 += ' '+j[6]+' '+j[7]+self.rs
                        print(print3)
                    else:
                        if verbosity == 3:
                            print4 = fg(8)+j[8]+': '+j[1]+' '+j[4]+' '+j[3]
                            print4 += ' '+j[6]+' '+j[7]+self.rs
                            print(print4)
            

    #Print AI out
    def ai_parse(self):
        self.ai_ad = []
        self.conn = apsw.Connection(self.dbfile)
        self.cursor = self.conn.cursor()
        select = 'SELECT requests.module,requests.url,requests.headers,'
        select += 'responses.responseSize,responses.statusCode,responses.time,'
        select += 'responses.numHeaders,responses.numTokens,requests.reqID '
        select += 'FROM requests INNER JOIN responses '
        select += 'ON responses.respID == requests.reqID'
        try:
            self.cursor.execute(select)
            resps = self.cursor.fetchall()
            for i in resps:
                data = {
                        "module": i[0],
                        "url": i[1],
                        "headers": i[2],
                        "responseSize": i[3],
                        "statusCode": i[4],
                        "time": i[5],
                        "numHeaders": i[6],
                        "numTokens": i[7],
                        "id": i[8]
                }
                self.ai_ad.append(data)
        except Exception as e:
            print(e)
        return self.ai_ad


    #Close the database connection
    def close(self):
        self.conn.close()        
