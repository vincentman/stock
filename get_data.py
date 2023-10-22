import yfinance as yf
from FinMind.data import DataLoader
import pandas as pd
from pandas_datareader import data
from datetime import datetime
import os

# import time

data_source_yfinance = 1
data_source_finmind = 2
data_source = data_source_yfinance

stock_name = 'TSLA'
stock_id = ['TSLA']
# stock_name = '勤誠_光寶科'
# stock_id = ['8210.TW', '2301.TW']  # yfinance format. 上櫃用TWO, 上市用TW?
# stock_name = '勤誠'
# stock_id = ['8210.TW']
# stock_name = '榮剛'
# stock_id = ['5009.TWO']
# stock_name = '光寶科'
# stock_id = ['2301.TW']
# stock_name = '台積電'
# stock_id = ['2330.TW']

start_date = datetime(2010, 1, 1)
# end_date = datetime.today().date()
end_date = datetime(2020, 6, 30)


def get_data_by_yfinance():
    # yf.pdr_override()  # 以pandasreader常用的格式覆寫
    # ret = data.get_data_yahoo(target_stock, start_date, end_date)  # 將資料放到Dataframe裡面
    ret = yf.download(stock_id, start=start_date, end=end_date) # 可使用 period = 6mo
    return ret


def get_data_by_finmind():
    dl = DataLoader()
    target_stock_tw = [i.replace(".TWO", "") for i in stock_id]
    target_stock_tw = [i.replace(".TW", "") for i in target_stock_tw]
    ret = dl.taiwan_stock_daily(stock_id=target_stock_tw, start_date=start_date.strftime('%Y-%m-%d'))
    return ret


if __name__ == '__main__':
    if data_source == data_source_yfinance:
        df = get_data_by_yfinance()
        data_folder = 'yfinance'
    elif data_source == data_source_finmind:
        df = get_data_by_finmind()
        data_folder = 'finmind'
    df.to_csv(os.path.join('data', data_folder, f'{stock_name}.csv'))
