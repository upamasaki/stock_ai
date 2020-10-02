# coding: utf-8

import json
import requests
from io import StringIO
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")

def main():
    # 株の名前
    stock_name = "AAPL"

    #############################################
    # 株データの生データのダウンロード
    #
    # download(stock_name)

    #############################################
    # 生データの前処理(UNIX時刻からの変換)
    #
    # preprocess(stock_name)

    #############################################
    # 描画(seabornを使用)
    #
    visual(stock_name)

def download(stock_name):

    # request URL
    URL = "https://query1.finance.yahoo.com/v7/finance/chart/{}?range=1d&interval=1m&indicators=quote&includeTimestamps=true".format(stock_name)

    # データの保存path
    csvpath = "./output/stock_origin_{}.csv".format(stock_name)

    # request
    r = requests.get(URL)
    s = StringIO(r.text)

    # json の取得
    j = json.load(s)

    # jsonからdataframeへの変換
    df = pd.DataFrame()
    df['timestamp'] = j['chart']['result'][0]['timestamp']
    df['open'] = j['chart']['result'][0]['indicators']['quote'][0]['open']
    df['low'] = j['chart']['result'][0]['indicators']['quote'][0]['low']
    df['high'] = j['chart']['result'][0]['indicators']['quote'][0]['high']
    df['close'] = j['chart']['result'][0]['indicators']['quote'][0]['close']
    df['volume'] = j['chart']['result'][0]['indicators']['quote'][0]['volume']

    # csvの保存
    df.to_csv(csvpath, index=False, encoding='utf8')

def preprocess(stock_name):

    # 読み込みデータのpath
    csvpath = "./output/stock_origin_{}.csv".format(stock_name)

    # 生データの読み込み
    df_read = pd.read_csv(csvpath)
    print(df_read)

    # 株の名前
    stock_name = "AAPL"

    # データの保存path
    csvpath = "./output/stock_{}.csv".format(stock_name)

    # 一行ずつ時刻の変換
    for i in range(len(df_read)):
        df_read.loc[i, 'time'] = datetime.fromtimestamp(df_read.loc[i, 'timestamp'])
        df_read.loc[i, 'stock_name'] = stock_name

    # 結果の出力
    print(df_read)

    # csvの保存
    df_read.to_csv(csvpath, index=False, encoding='utf8')

def visual(stock_name):
    # 読み込みデータのpath
    csvpath = "./output/stock_{}.csv".format(stock_name)

    # Load an example dataset with long-form data
    df = pd.read_csv(csvpath)

    # 図のサイズ指定
    fig = plt.figure(figsize=(30, 10))


    # Plot the responses for different events and regions
    sns.lineplot(x="time",
                 y="open",
                 hue="stock_name",
                 data=df)

    # 図の保存path
    figpath = "./output/stock_{}_fig.png".format(stock_name)

    # 図の保存
    plt.savefig(figpath)  # save as png file


if __name__ == '__main__':
    main()
