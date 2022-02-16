import numpy as np
import os
import glob

from get_symbols import get_symbols
from get_nepse_datav2 import get_nepse_data
import multiprocessing
from issue_symbols import issue_sybmols
from data_process import data_process


def remove_prev_files():
    folders = ['data', 'temp', 'log']
    files = ['issue_symbols.txt']
    for folder in folders:
        fs = glob.glob(folder + '/*')
        for f in fs:
            if os.path.exists(f):
                os.remove(f)
    for f in files:
        if os.path.exists(f):
            os.remove(f)

if __name__ == '__main__':
    remove_prev_files()

    symbols = get_symbols()
    threads_count = 20
    symbols_split = np.array_split(symbols,threads_count)

    threads = [multiprocessing.Process(target=get_nepse_data, args=(symbols_split[i],i,)) for i in range(threads_count)]

    for x in range(threads_count):
        threads[x].start()

    for x in range(threads_count):
        threads[x].join()

    sym = issue_sybmols()
    print("Symbols that count't be downloaded: ")
    print(sym)


    data_process()



