import json

from get_nepse_datav2 import hash_symbol
from data_process import date_converter

filename = hash_symbol('BANKING')


f = open ("data/" + filename, "r")
data = json.loads(f.read())
f.close()

total_records = len(data['t'])
dates = date_converter(data['t'])


print(data['c'])

