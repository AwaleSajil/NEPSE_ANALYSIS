import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt


def calculate_bollinger_band(df, length = 20, std_dev = 2):

    # Clean NaN values
    df = dropna(df)

    # Initialize Bollinger Bands Indicator
    indicator_bb = BollingerBands(close=df["close"], window=length, window_dev=std_dev)

    # Add Bollinger Bands features
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    # Add Bollinger Band high indicator
    df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

    # Add Bollinger Band low indicator
    df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

    return df

if __name__ == '__main__':
    df = pd.read_csv('../../NEPSE_DATA_LOADER/Nepse_raw_data_Oct-15-2021.csv', parse_dates=True)
    df = df.set_index('date')
    nepse = df[df['symbol'] == 'NEPSE']
    x = calculate_bollinger_band(nepse[['close']], length = 20)
    x = x[x.index > '2021-01-01']
    print(x)
    x.plot()
    plt.show()

