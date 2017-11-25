import csv
import json
import os
import os.path

from pathlib import Path

from providers.Converter import Converter

config = json.load(open('./config.json'))

data_csv = []
with open('./data.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in data:
        data_csv.append( ', '.join(row).split(',') )
table = str(input("\n\nTable: ")) 

print("\n\n START ..\n\n")

_str = []

for d in data_csv:
    _str_insert = ""
    for datas in d:
        _str_insert = _str_insert + '\''+ datas + '\',' 

    _str.append(_str_insert)

initital_query = []

_str_insert = "("

part_query = []

for key, value in enumerate(config):
    if key != 0:
        _str_insert = _str_insert + ',' + value +  ''
    else:
        _str_insert = _str_insert + '' + value +  ''

_str_insert = _str_insert + ")"

for dc in data_csv:
    final_query = " VALUE ("
    for key, q_s in enumerate(dc):
        if key != 0:
            final_query = final_query + ',' + q_s
        else:
            final_query = final_query + q_s
    final_query += ")"
    part_query.append(final_query)

final_query = []

for q in part_query:
    final_query.append("INSERT INTO " + table + _str_insert + q)

direc = './querys_file/'+ table + '/'
path_name = direc + table + '.sql'

file_path = Path(path_name)

directory = os.path.dirname(file_path)

if not os.path.exists(directory):
    os.makedirs(directory)
else:  
    num_of_file = len([f for f in os.listdir(direc)
                if os.path.isfile(os.path.join(direc, f))])
    path_name = path_name.split('.sql')[0] + '_' + str(num_of_file) + '.sql'

file = open(path_name, 'w')

for f_q in final_query:
    file.write(f_q+'\n')
    # print(f_q)

file.close()

print("\n\n END ..")