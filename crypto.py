import os
import requests
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

rn_url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
hist_url = 'https://api.coindesk.com/v1/bpi/historical/close.json'


def query_current_price(url):
    response = requests.get(url)
    r = response.json()
    price = r['bpi']
    dead_prez = price['USD']
    time = r['time']
    rn = time['updated']
    return (rn, round(float(dead_prez['rate'].replace(',', ''))))


def query_historical_price(url):
    response = requests.get(url)
    r = response.json()
    prices = r['bpi']

    clean_prices = tuple(prices.items())
    cleaner_prices = [(date[5:], round(price)) for date, price in clean_prices]
    return cleaner_prices


def plot_historical(prices):
    zip(*prices)

    chart_title = "BTC-USD Exchange Rate - Past 10 Days"
    print(chart_title)
    print("-" * len(chart_title))

    fig, ax = plt.subplots()
    ax.plot(*zip(*prices))
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.set_title(chart_title)
    plt.show()


def data_analysis(df):
    print('Average price (Last 31 days): $', round(df['BTC-USD'].mean()))
    print('High (Last 31 days): $', df['BTC-USD'].max())
    print('Low (Last 31 days): $', df['BTC-USD'].min())


def build_dataframe(pricelist):
    return pd.DataFrame.from_records(pricelist, columns=['Date', 'BTC-USD'])


def create_dataset(dataframe, name, filename, database):
    sql_command = ('sudo mysql -u root -pcodio -e "CREATE DATABASE '
                   + 'IF NOT EXISTS ' + database + ';"')

    os.system(sql_command)
    dataframe.to_sql(name, con=createEngine(database), if_exists='replace',
                     index=False)
    save_database(filename, database)


def load_dataset(filename, database, table_name):
    sql_command = ('sudo mysql -u root -pcodio -e "CREATE DATABASE '
                   + 'IF NOT EXISTS ' + database + ';"')

    os.system(sql_command)
    os.system("sudo mysql -u root -pcodio" + database + " < " + filename)
    df = pd.read_sql_table(table_name, con=createEngine(database))
    return df


def createEngine(database):
    return create_engine('mysql://root:codio@localhost/' +
                         database + '?charset=utf8', encoding='utf8')


def save_database(filename, database):
    os.system("mysqldump -u root -pcodio " + database + " > " + filename)


def main():
    filename = 'crypto.sql'
    database = 'crypto'

    query_time, btc_cost = query_current_price(rn_url)
    format_time = query_time + ','
    print('As of', format_time, '1 BTC currently costs $', btc_cost, 'USD!')

    # create dataset from scratch
    cleaner_prices = query_historical_price(hist_url)
    cleanest_prices = cleaner_prices[21:]

    full_df = build_dataframe(cleaner_prices)
    data_analysis(full_df)

    plot_historical(cleanest_prices)

    # df = load_dataset(filename, database, 'historical')
    create_dataset(full_df, 'historical', filename, database)

    # save_dataset()

    print("Look at that price fluctuation!")
    print("Crypto is the future, but it's still in early stages.")


if __name__ == "__main__":
    main()
