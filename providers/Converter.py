#encoding: utf-8
import unicodedata
import csv
import json
import os
from pathlib import Path

class Converter():
    def __init__(self):
        self.table = str(input("Table: "))
        self.config = []
        self.dataCsv = []
        self.final_query = []
    def setConfig(self):
        self.config = json.load(open('./config.json'))
    def setCsvData(self):
        with open('./data.csv', newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in data:
                self.dataCsv.append( ','.join(row).split(',') )
    def printsDatas(self):
        print( self.final_query )
    def setInsert(self):
        _str = []
        for d in self.dataCsv:
            _str_insert = ""
            for datas in d:
                _str_insert = _str_insert + '\''+ datas + '\',' 
            _str.append(_str_insert)
        _str_insert = "("
        part_query = []
        for key, value in enumerate(self.config):
            if key != 0:
                _str_insert = _str_insert + ',' + value 
            else:
                _str_insert = _str_insert + value 
        _str_insert = _str_insert + ")"
        for dc in self.dataCsv:
            final_query = " VALUES ("
            for key, q_s in enumerate(dc):
                if '\'' in q_s:
                   q_s = q_s.replace('\'',"\'\'")
                   q_s = unicodedata.normalize('NFD', q_s).encode('ascii', 'ignore')
                if key != 0:
                    final_query = final_query + ',' + "\'" + str(q_s) + "\'"
                else:
                    final_query = final_query + "\'" + str(q_s) + "\'"
            final_query += ");"
            part_query.append(final_query)
        final_query = []
        for q in part_query:
            final_query.append("INSERT INTO " + self.table + _str_insert + q)
        self.final_query = final_query
    def saveFile(self):                
        direc = './querys_file/'+ self.table + '/'
        path_name = direc + self.table + '.sql'
        file_path = Path(path_name)
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:  
            num_of_file = len([f for f in os.listdir(direc)
                        if os.path.isfile(os.path.join(direc, f))])
            path_name = path_name.split('.sql')[0] + '_' + str(num_of_file) + '.sql'
        file = open(path_name, 'w')
        for f_q in self.final_query:
            file.write(f_q+'\n')
            # print(f_q)
        file.close()

    def start(self):
        self.setCsvData()   
        self.setConfig()
        self.setInsert()
        self.printsDatas()
        self.saveFile()