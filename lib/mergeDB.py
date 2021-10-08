#This class binds .db databases together
#Pass in a list of sqlite dbs and an output filename
import os
import sys
import argparse
import sqlite3

class MergeDBs:
    def __init__(self, list_of_dbs, output_db):
        self.dblist = list_of_dbs
        self.output = output_db
        self.old_db = None
        self.new_db = None

    def joinDB(self, db_1, db_2name):
        attach = 'ATTACH \''+db_2name+'\' as dba'
        db_1.execute(attach)
        db_1.execute('BEGIN')
        
        selects = 'SELECT * FROM dba.sqlite_master WHERE type=\'table\''
        for row in db_1.execute(selects):
            combine = 'INSERT INTO '+row[1]+' SELECT * FROM dba.'+row[1]
            db_1.execute(combine)
        db_1.commit()
        db_1.execute('DETACH DATABASE dba')
        return db_1

    def processList(self):
        if len(self.dblist) > 1:
            for i in range(0, len(self.dblist)):
                if i == 0:
                    command = 'cp '+self.dblist[i]+' '+self.output
                    os.system(command)
                    self.old_db = sqlite3.connect(self.output)
                else:
                    self.new_db = self.joinDB(self.old_db, self.dblist[i])
                    self.old_db = self.new_db
            self.old_db.close()
