from backtesting import Backtest, Strategy  # 引入回測和交易策略功能
from backtesting.lib import crossover  # 從lib子模組引入判斷均線交會功能
from backtesting.test import SMA  # 從test子模組引入繪製均線功能
import pandas as pd  # 引入pandas讀取股價歷史資料CSV檔
import os

# stock_name = "TSLA"
# stock_name = "榮剛"
# stock_name = "光寶科"
# stock_name = "勤誠"
stock_name = "台積電"

data_source_yfinance = 1
data_source_finmind = 2
data_source = data_source_yfinance


class SmaCross(Strategy):  # 交易策略命名為SmaClass，使用backtesting.py的Strategy功能
    n1 = 5  # 設定第一條均線日數為5日(周線)
    n2 = 20  # 設定第二條均線日數為20日(月線)，這邊的日數可自由調整

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)  # 定義第一條均線為sma1，使用backtesting.py的SMA功能算繪
        self.sma2 = self.I(SMA, self.data.Close, self.n2)  # 定義第二條均線為sma2，使用backtesting.py的SMA功能算繪

    def next(self):
        if crossover(self.sma1, self.sma2):  # 如果周線衝上月線，表示近期是上漲的，則買入
            self.buy()
        elif crossover(self.sma2, self.sma1):  # 如果周線再與月線交叉，表示開始下跌了，則賣出
            self.sell()


def my_print(contents, output_file=None):
    print(contents)
    if output_file:
        print(contents, file=output_file)


if __name__ == '__main__':
    if data_source == data_source_yfinance:
        data_folder = 'yfinance'
    elif data_source == data_source_finmind:
        data_folder = 'finmind'
    file_path = os.path.join('data', data_folder, f'{stock_name}.csv')
    df = pd.read_csv(file_path)  # pandas讀取資料，並將第1欄作為索引欄
    df = df.interpolate()  # CSV檔案中若有缺漏，會使用內插法自動補值，不一定需要的功能
    df['Date'] = pd.to_datetime(df['Date'])  # 將索引欄資料轉換成pandas的時間格式，backtesting才有辦法排序
    df = df.set_index('Date')  # set date as index

    # 指定回測程式為test，在Backtest函數中依序放入(資料來源、策略、現金、手續費)
    test = Backtest(df, SmaCross, cash=10000, commission=.004)
    # 執行回測程式並存到result中
    result = test.run()
    with open(f"./backtest_result/{stock_name}_result.txt", 'w') as out_file:
        my_print('%s' % result, out_file)
    test.plot(filename=f"./backtest_result/{stock_name}_plot.html", open_browser=False)  # 將線圖網頁依照指定檔名保存
