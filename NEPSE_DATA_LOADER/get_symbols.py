import pandas as pd
import subprocess
import json
import os

devnull = open(os.devnull, 'w')


def get_symbols():
    text = """curl "https://nepsealpha.com/trading/1/search?limit=30&query=&type=&exchange=" \
  -H "sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"" \
  -H "Referer: https://nepsealpha.com/trading/chart" \
  -H "sec-ch-ua-mobile: ?0" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36" \
  -H "sec-ch-ua-platform: "Windows""
  --output _get_symbols_temp.txt"""
    p1 = subprocess.call(text, stdout=devnull, stderr=devnull)
    f = open ('_get_symbols_temp.txt', "r")
    data = json.loads(f.read())
    symbols_df = pd.DataFrame(data)
    symbols_df = symbols_df.set_index('symbol')
    symbols_df.to_csv('NEPSE_symbols.csv')
    symbols = symbols_df.index.to_numpy()
    return symbols
