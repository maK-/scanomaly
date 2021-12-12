#This class parses a data from SQLite and imports into MeiliSearch
import os
import sys
import argparse
import meilisearch
import uuid

class MeiliS:
    def __init__(self, dbformat, index_string):
        self.dbdata = dbformat
        self.documents = []
        self.client = meilisearch.Client('http://127.0.0.1:7700')
        self.index = self.client.index(index_string)

    #Import all the formatted data into Meilisearch
    def import_all(self):
        for i in range(0, len(self.dbdata)):
            self.documents.append(self.parse_tuple(self.dbdata[i], i))
        
        self.index.add_documents(self.documents)
        return True

        """
        0. requests.module
        1. requests.url
        2. requests.headers
        3. responses.responseSize
        4. responses.statusCode
        5. responses.time
        6. responses.numHeaders
        7. responses.numTokens
        8. requests.method
        9. responses.content
        10. responses.headers
        11. requests.reqID 
        """

    def parse_tuple(self, data_tuple, id_val):
        data = {
                'id': str(uuid.uuid1()),
                'reqID': str(data_tuple[11]),
                'method': str(data_tuple[8]),
                'module': str(data_tuple[0]),
                'url': str(data_tuple[1]),
                'status': str(data_tuple[4]),
                'request.headers': str(data_tuple[2]),
                'response.headers': str(data_tuple[10]),
                'size': str(data_tuple[3]),
                'title': self.get_title(data_tuple[9])
                #'content': str(data_tuple[9]) Removed
        }
        print(data)
        return data
        
    #Get title from content
    def get_title(self, content):
        t1 = ''
        t2 = ''
        if '<title>' in content:
            t1 = content.split('<title>')[1]
            t2 = t1.split('</title>')[0]
        elif '<TITLE>' in content:
            t1 = content.split('<TITLE>')[1]
            t2 = t1.split('</TITLE>')[0]

        if len(t2) > 0 and len(t2) < 250:
            return t2
        else:
            return ''
