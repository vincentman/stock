from backtesting import Backtest, Strategy  # 引入回測和交易策略功能

from backtesting.lib import crossover  # 從lib子模組引入判斷均線交會功能
from backtesting.test import SMA  # 從test子模組引入繪製均線功能

import pandas as pd  # 引入pandas讀取股價歷史資料CSV檔

stock = "TSLA"  # 設定要測試的股票標的名稱
# stock = "勤誠"  # 設定要測試的股票標的名稱


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
    df = pd.read_csv(f"./data/{stock}.csv", index_col=0)  # pandas讀取資料，並將第1欄作為索引欄
    # df = df.interpolate()  # CSV檔案中若有缺漏，會使用內插法自動補值，不一定需要的功能
    df.index = pd.to_datetime(df.index)  # 將索引欄資料轉換成pandas的時間格式，backtesting才有辦法排序

    # 指定回測程式為test，在Backtest函數中依序放入(資料來源、策略、現金、手續費)
    test = Backtest(df, SmaCross, cash=10000, commission=.002)
    # 執行回測程式並存到result中
    result = test.run()
    with open(f"./backtest_result/{stock}_result.txt", 'w') as out_file:
        my_print('%s' % result, out_file)
    # test.plot(filename=f"./backtest_result/{stock}_plot.html")  # 將線圖網頁依照指定檔名保存
