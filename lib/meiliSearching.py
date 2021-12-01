#This class parses a data from SQLite and imports into MeiliSearch
import os
import sys
import argparse
import meilisearch

class MeiliS:
    def __init__(self, dbformat):
        self.dbdata = dbformat
        self.documents = []
        self.client = meilisearch.Client('http://127.0.0.1:7700')
        self.index = self.client.index('scanomaly')

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
                'id': int(id_val),
                'reqID': str(data_tuple[11]),
                'module': str(data_tuple[0]),
                'url': str(data_tuple[1]),
                'method': str(data_tuple[8]),
                'content': str(data_tuple[9])
        }
        print(data)
        return data
        
            
        
         
