from PyNomaly import loop
from colored import fg, bg, attr
import numpy as np


class AnomalyDetect:

    def __init__(self, dbdata):
        self.rs = attr('reset')
        self.dbdata = dbdata
        self.test200 = []
        self.test301 = []
        self.other = []

    def getByStatus(self):
        for i in self.dbdata:
            if i['statusCode'] == "200":
                self.test200.append([
                                        i['id'],
                                        int(i['responseSize']),
                                        int(i['numHeaders']),
                                        int(i['numTokens'])
                                    ])
            elif i['statusCode'] == "301":
                self.test301.append([
                                        i['id'],
                                        int(i['responseSize']),
                                        int(i['numHeaders']),
                                        int(i['numTokens'])
                                    ])
            else:
                self.other.append([
                                    i['id'],
                                    int(i['responseSize']),
                                    int(i['numHeaders']),
                                    int(i['numTokens'])
                                  ])
        try:
            print('\n==200==')
            self.getScores(self.test200)
        except:
            print('None Found!')
        
        try:
            print('\n==301==')
            self.getScores(self.test301)
        except:
            print('None Found!')
        
        try:
            print('\n==Others==')
            self.getScores(self.other)
        except:
            print('None Found!')

    def getScores(self, inputs):
        store_ids = []
        store_arrays = []

        for i in range(0, len(inputs)):
            entry = inputs[i]
            store_ids.append(entry.pop(0))
            ai_data = entry
            store_arrays.append(ai_data)
        data = np.array(inputs)
        if len(data) != 0:
            outliers = loop.LocalOutlierProbability(data, 
                        n_neighbors=3).fit().local_outlier_probabilities

        baseline_count = 0
        self.printHead()
        for i in range(0, len(inputs)):
            if outliers[i] > 0.0:
                self.printResp(store_ids[i])
            else:
                baseline_count += 1
        print('(+) There were '+str(baseline_count)+' entries removed!')



    def printHead(self):
        forprint = fg(1)+'Module: '+self.rs+'URL '+fg(4)+'status '+fg(10)
        forprint += 'size '+fg(3)+'time '+fg(13)+'numHeaders '+fg(14)
        forprint += 'numTokens'+fg(8)+' headers'+self.rs
        print(forprint)


    def printResp(self, rid):
        for i in self.dbdata:
            if i['id'] == rid:
                response = fg(1)+i['module']+self.rs+': '+self.rs+i['url']+' '
                response += fg(4)+i['statusCode']+' '+fg(10)+i['responseSize']
                reponse += ' '+fg(3)+i['time']+' '+fg(13)+i['numHeaders']+' '
                response += fg(14)+i['numTokens']+' '+fg(8)+i['headers']+self.rs
                print(response)

