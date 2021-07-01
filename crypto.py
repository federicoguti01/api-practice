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
    return cleaner_prices[21:]


def plot_historical(prices):
    zip(*prices)

    chart_title = "BTC-USD Exchange Rate - Past 10 Days"
    print(chart_title)
    print("-" * len(chart_title))

    fig, ax = plt.subplots()
    ax.plot(*zip(*prices))
    fig.show()


def build_dataframe(pricelist):
    return pd.DataFrame.from_records(pricelist, columns=['Date', 'BTC-USD'])


def create_database_table(dataframe, name):
    engine = create_engine('mysql://root:codio@localhost/crypto')
    dataframe.to_sql(name, con=engine, if_exists='replace', index=False)
    save_database()


def load_database():
    os.system("mysql -u root -pcodio crypto < crypto.sql")


def save_database():
    os.system("mysqldump -u root -pcodio crypto > crypto.sql")


def main():
    query_time, btc_cost = query_current_price(rn_url)
    cleanest_prices = query_historical_price(hist_url)
    format_time = query_time + ','

    print('As of', format_time, '1 BTC currently costs $', btc_cost, 'USD!')

    plot_historical(cleanest_prices)

    df = build_dataframe(cleanest_prices)
    create_database_table(df, 'historical')

    # load_database()
    # save_database()

    print("Look at that price fluctuation!")
    print("Crypto is the future, but it's still in early stages.")


if __name__ == "__main__":
    main()
