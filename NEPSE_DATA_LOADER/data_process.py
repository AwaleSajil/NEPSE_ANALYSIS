import pandas as pd
import time
from datetime import date
import os
import json 


def date_converter(unix_epoch_list):
    result = []
    for unix_epoch in unix_epoch_list:
        x = time.strftime('%Y-%m-%d', time.localtime(unix_epoch))
        result.append(x)
    return result


def correct_duplicate_date_data(data):
    all_dates = date_converter(data['t'])
    stage1_dict = dict()
    stage2_dict = {"date": [],
                    "close": [],
                    "open": [],
                    "high": [],
                    "low": [],
                    "volume": []}

    for i, date_i in enumerate(all_dates):
        stage1_dict[str(date_i)] = [data['c'][i], data['o'][i], data['h'][i], data['l'][i], data['v'][i]]
    
    for date_i in stage1_dict.keys():
        ct,ot,ht,lt,vt = stage1_dict[date_i]
        stage2_dict["date"].append(date_i)
        stage2_dict["close"].append(ct)
        stage2_dict["open"].append(ot)
        stage2_dict["high"].append(ht)
        stage2_dict["low"].append(lt)
        stage2_dict["volume"].append(vt)
    return stage2_dict



def data_process():
    today = date.today()
    column_names = ["date", "close", "open", "high", "low", "volume", "symbol"]
    df = pd.DataFrame(columns = column_names)
    df.set_index('date')

    for name in os.listdir("data/"):
        f = open ("data/" + name, "r")
        data = json.loads(f.read())
        if 's' in data.keys() and data['s'] == 'ok':
            sym_data = correct_duplicate_date_data(data)
            sym_data["symbol"] =  [data['symbol']]*len(sym_data['date'])
            df_temp = pd.DataFrame(sym_data)
            df_temp.set_index('date')

            df = pd.concat([df, df_temp])
    df.to_csv('Nepse_raw_data_' + today.strftime("%b-%d-%Y") +  '.csv')

   

# data_process()