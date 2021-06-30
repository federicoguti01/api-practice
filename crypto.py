import requests
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

rn_url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
hist_url = 'https://api.coindesk.com/v1/bpi/historical/close.json'

response = requests.get(rn_url)
r = response.json()
price = r['bpi']
dead_prez = price['USD']
btc_cost = round(float(dead_prez['rate'].replace(',','')))

time = r['time']
rn = time['updated']
format_rn = rn + ','

print('As of', format_rn, '1 Bitcoin currently costs $', btc_cost, 'USD!')

response = requests.get(hist_url)
r = response.json()
prices = r['bpi']

clean_prices = tuple(prices.items())
cleaner_prices = [(date[5:], round(price)) for date, price in clean_prices]
cleanest_prices = cleaner_prices[21:]

zip(*cleanest_prices)

chart_title = "BTC-USD Exchange Rate - Past 10 Days"
print(chart_title)
print("-" * len(chart_title))

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(*zip(*cleanest_prices))

df = pd.DataFrame.from_records(cleanest_prices, columns=['Date', 'BTC-USD'])

engine = create_engine('mysql://root:codio@localhost/crypto')
df.to_sql('historical_btc', con=engine, if_exists='replace', index=False)

print("Look at that price fluctuation!")
print("Crypto is the future, but it's still in early stages.")