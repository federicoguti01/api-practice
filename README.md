# Crypto API Script

## This project displays the latest price for Bitcoin
![Bitcoin Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/BTC_Logo.svg/1920px-BTC_Logo.svg.png)
## It also displays historical prices for the past 10 days.

Vitalik Buterin:
> Whereas most technologies tend to automate workers on the periphery doing menial tasks, blockchains automate away the center. Instead of putting the taxi driver out of a job, blockchain puts Uber out of a job and lets the taxi drivers work with the customer directly.

Bitcoin and, more broadly, blockchain is undoubtedly a technology that is here to stay.
This program aims to visualize the BTC-USD exchange rate, which remains very volatile.
This is not financial advice~~, but if you don't believe in crypto I'll kill you~~!

## Descripton of algorithm:

This algorithm does many things.
- It prints the current price of Bitcoin.
- It plots the Bitcoin's performance in the last 10 days on a line graph.
- It uploads the historical data into a SQL database, but not before converting it into a pandas dataframe!
---
## Guide:

If creating the database for the first time, **use create_database_table(), with the dataframe and desired table name as parameters**.
If you just want to edit/update the table, **use load_database() and edit with MySQL, then use save_database()**.

### External info:

Current BTC-USD exchange rate is taken from the Bitcoin Price Index, courtesy of [Coindesk](https://www.coindesk.com/).

[Click here for API information](https://www.coindesk.com/coindesk-api)