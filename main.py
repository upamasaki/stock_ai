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
    # preprocess()
    visual()

def download():

    stock_name = "AAPL"
    URL = "https://query1.finance.yahoo.com/v7/finance/chart/{}?range=1d&interval=1m&indicators=quote&includeTimestamps=true".format(stock_name)
    csvpath = "./output/stock_origin_{}.csv".format(stock_name)

    r = requests.get(URL)
    s = StringIO(r.text)
    j = json.load(s)

    df = pd.DataFrame()
    df['timestamp'] = j['chart']['result'][0]['timestamp']
    df['open'] = j['chart']['result'][0]['indicators']['quote'][0]['open']
    df['low'] = j['chart']['result'][0]['indicators']['quote'][0]['low']
    df['high'] = j['chart']['result'][0]['indicators']['quote'][0]['high']
    df['close'] = j['chart']['result'][0]['indicators']['quote'][0]['close']
    df['volume'] = j['chart']['result'][0]['indicators']['quote'][0]['volume']

    df.to_csv(csvpath, index=False, encoding='utf8')

def preprocess():
    df_read = pd.read_csv('./output/out.csv')
    print(df_read)

    now = datetime.now()
    print(now)

    now_from_ts = datetime.fromtimestamp(1601386200)
    print(now_from_ts)

    stock_name = "AAPL"

    csvpath = './output/out2.csv'
    for i in range(len(df_read)):
        df_read.loc[i, 'time'] = datetime.fromtimestamp(df_read.loc[i, 'timestamp'])
        df_read.loc[i, 'stock_name'] = stock_name
    print(df_read)
    df_read.to_csv(csvpath, index=False, encoding='utf8')

def visual():


    # Load an example dataset with long-form data
    df = pd.read_csv('./output/out2.csv')

    fig = plt.figure(figsize=(30, 10))
    # Plot the responses for different events and regions
    sns.lineplot(x="time",
                 y="open",
                 hue="stock_name",
                 data=df)
    # sns.lineplot(x="time",
    #              y="close",
    #              hue="stock_name",
    #              data=df)
    plt.savefig("seaborntest.png")  # save as png file

    # # Load an example dataset with long-form data
    # fmri = sns.load_dataset("fmri")
    # print(fmri)
    #
    # fig = plt.figure() #わからない2
    # # Plot the responses for different events and regions
    # sns.lineplot(x="timepoint", y="signal",
    #              hue="region", style="event",
    #              data=fmri)
    # plt.savefig("seaborntest2.png")  # save as png file

if __name__ == '__main__':
    main()
