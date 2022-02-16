import pandas as pd
from ta.utils import dropna
from ta.momentum import RSIIndicator
import matplotlib.pyplot as plt

def calculate_simple_rsi(df, length = 14):
    # expected input
    # data = data frame with index as date and another col of closed price
    # length = int for simple moving average
    df = dropna(df)
    rsi_instance = RSIIndicator(df['close'], length)
    df['rsi'] = rsi_instance.rsi()
    return df


if __name__ == '__main__':
    df = pd.read_csv('../../NEPSE_DATA_LOADER/Nepse_raw_data_Oct-15-2021.csv', parse_dates=True)
    df = df.set_index('date')
    nepse = df[df['symbol'] == 'NEPSE']
    x = calculate_simple_rsi(nepse[['close']], length = 14)
    x = x[x.index > '2021-01-01']
    print(x)
    x.plot()
    plt.show()

