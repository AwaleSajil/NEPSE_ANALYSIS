import subprocess
import time
from datetime import datetime
import json
import os
import time
import hashlib


def hash_symbol(symbol):
    result = hashlib.sha256(symbol.encode())
    return str(result.hexdigest())

def request_text(symbol, stop_date_epoch):
  temp_loc = 'temp/' + hash_symbol(symbol)
  uri  = "https://nepsealpha.com/trading/1/history?symbol=%(sym)s&resolution=1D&from=0&to=%(stop_date)s&currencyCode=NRS"

  reqi = """curl \"""" + uri % {"sym": symbol, "stop_date": stop_date_epoch} + """\"    \
  -H "Connection: keep-alive" \
  -H "sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"" \
  -H "sec-ch-ua-mobile: ?0" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36" \
  -H "sec-ch-ua-platform: "Windows"" \
  -H "Accept: */*" \
  -H "Sec-Fetch-Site: same-origin" \
  -H "Sec-Fetch-Mode: cors" \
  -H "Sec-Fetch-Dest: empty" \
  -H "Referer: https://nepsealpha.com/trading/chart" \
  -H "Accept-Language: en-US,en;q=0.9" \
  -H "Cookie: _ga=GA1.1.1562869078.1634024480; laravel_session=eyJpdiI6IkZDQm9CUmNVYjByWG5TSTRjTGtwL3c9PSIsInZhbHVlIjoiSkZ2N1JxeFdjN3plMktCWW9scjR4cXc0YXFHQmgzVTRHQ3dwdFliNm1MbElCVWxwYVJwK2FZeG5iSFlmaVlGazVHdUova3R4SU8xYUhkT1RaYnQvbFNMMzVORlZYS3dkVGR1aWJYUWcrYWUwL1RFNnZicHQ4ZE9pUzVYSXU2ZDgiLCJtYWMiOiIyODFlZjE4YzMyN2UyY2JlYTYzZTIyMjc5ODE2Mjc4Y2Y5ZjBkMDBlN2M4ODZjODJlYjQ1ZGE5ZjZjOWE2NjUxIn0%3D; _ga_LBBQFT2KX1=GS1.1.1634266915.12.1.1634266953.0" """ \
  + " --output " + temp_loc

  return reqi





def get_nepse_data(local_symbols, thread_number):
    devnull = open(os.devnull, 'w')
    symbols = local_symbols

    stop_date = datetime.today().strftime('%Y-%m-%d')
    stop_date_epoch = int(time.mktime(datetime.strptime(stop_date, "%Y-%m-%d").timetuple())) + 50000000

    # log.write("Starting thread")
    for i, symbol in enumerate(symbols):
        log = open ('log/'+ hash_symbol(symbol), "w")
        log.write("------------------------Downloading for: " + symbol + '----------------------\n')
        print("Downloading for: " + symbol + " with thread: " + str(thread_number))
        text = request_text(symbol, stop_date_epoch)
        log.write("request:\n")
        log.write(text)
        p1 = subprocess.call(text, stdout=devnull, stderr=devnull)
        f = open ('temp/' + hash_symbol(symbol), "r")
        data = json.loads(f.read())
        data["symbol"] = symbol
        f.close()
        with open('data/' + hash_symbol(symbol), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        time.sleep(1)
        log.write("\n------------Finished Downloading: " + symbol + '-----------------')
    return 0
  