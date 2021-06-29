import requests

url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'


response = requests.get(url)
r = response.json()
price = r['bpi']
dead_prez = price['USD']
btc_cost = dead_prez['rate']

time = r['time']
rn = time['updated']
format_rn = rn + ','

print('As of', format_rn, '1 Bitcoin currently costs $', btc_cost, 'USD!')