import yfinance as yf
from FinMind.data import DataLoader
import pandas as pd
from pandas_datareader import data
from datetime import datetime

# import time

data_source_yfinance = 1
data_source_finmind = 2
data_source = data_source_yfinance

# target_name = '勤誠_光寶科'
# target_stock = ['8210.TW', '2301.TW']  # 股票代號變數
# target_name = '勤誠'
# target_stock = ['8210']  # 股票代號變數
target_name = '榮剛'
target_stock = ['5009.TWO']  # 股票代號變數

start_date = datetime(2019, 1, 1)
end_date = datetime.today().date()  # 設定資料起訖日期


def get_data_by_yfinance():
    # yf.pdr_override()  # 以pandasreader常用的格式覆寫
    # ret = data.get_data_yahoo(target_stock, start_date, end_date)  # 將資料放到Dataframe裡面
    ret = yf.download(target_stock, start=start_date)
    return ret


def get_data_by_finmind():
    dl = DataLoader()
    target_stock_tw = [i.replace(".TWO", "") for i in target_stock]
    ret = dl.taiwan_stock_daily(stock_id=target_stock_tw, start_date=start_date.strftime('%Y-%m-%d'))
    return ret


if data_source == data_source_yfinance:
    df = get_data_by_yfinance()
elif data_source == data_source_finmind:
    df = get_data_by_finmind()
filename = f'./data/{target_name}.csv'  # 以股票名稱命名檔案，放在data資料夾下面
df.to_csv(filename)  # 將df轉成CSV保存
