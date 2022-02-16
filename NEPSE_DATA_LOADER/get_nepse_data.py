import subprocess
import time
from datetime import datetime
import json
import os
import time
import hashlib


def request_text(symbol, stop_date_epoch, thread_number):
  temp_loc = 'temp/' + str(thread_number) + '_temp.txt'
  uri  = "https://nepsealpha.com/trading/1/history?symbol=%(sym)s&resolution=1D&from=0&to=%(stop_date)s&currencyCode=NRS"

  reqi = """curl \"""" + uri % {"sym": symbol, "stop_date": stop_date_epoch} + """\"  \
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
  -H "Cookie: _ga=GA1.1.1562869078.1634024480; _ga_LBBQFT2KX1=GS1.1.1634052701.6.1.1634053713.0; laravel_session=eyJpdiI6IkdQdjQ4a2R1bmtsMDUrUSsrUzVYTlE9PSIsInZhbHVlIjoiUTdUZ05zaS9oUlNKOHQwK2szMTd2bm1kblZJQyttMmdydTVtKzMva2hDRUNxelhJMU5tRzZLRUVEWXRudVBhMkxyVXR3VVRib1VWT3VNU3ZTdExTZzFtcXh6TzN4Zk5tZStweDcxNHZMY1BJVU56ekVmbWtFbGVPb0RNRUI0cDkiLCJtYWMiOiI2OWJmMGYwNTIyZjgzNTc1NGE5NjY1MzA0MTZmMjAzZDcxNzQzYzA2NWE3MDg0N2ExYjFlMmFmNGU0MGNhOGRiIn0%3D" """ \
  + " --output " + temp_loc

  return reqi





def get_nepse_data(local_symbols,thread_number):
    log = open ('log/log_' + str('_')  + str(thread_number) + '.txt', "w")
    devnull = open(os.devnull, 'w')
    symbols = local_symbols

    stop_date = datetime.today().strftime('%Y-%m-%d')
    stop_date_epoch = int(time.mktime(datetime.strptime(stop_date, "%Y-%m-%d").timetuple()))

    log.write("Starting thread")
    for i, symbol in enumerate(symbols):
        log.write("------------------------Downloading for: " + symbol + '----------------------')
        print("Downloading for: " + symbol + " with thread: " + str(i))
        text = request_text(symbol, stop_date_epoch,thread_number)
        log.write("request:")
        log.write(text)
        p1 = subprocess.call(text, stdout=devnull, stderr=devnull)
        f = open ('temp.txt', "r")
        data = json.loads(f.read())
        data["symbol"] = symbol
        f.close()
        with open('data/' + str(thread_number) + '_' + str(i) + '.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        time.sleep(2)
    log.write("------------Finished task for thread: " + thread_number + '-----------------')
    return 0
  