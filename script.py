import requests
import os
from dotenv import load_dotenv
import csv
import time

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000

def run_stock_job():
    url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    tickers =[]

    data = response.json()
    api_call_count = 1  # Track API calls
    ## print(data.keys())
    for ticker in data['results']:
        tickers.append(ticker)

    while 'next_url' in data:
        if api_call_count % 5 == 0:
            # print('Sleeping for >1 minute to respect API rate limits of 5 calls per minute')
            time.sleep(65)
        response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
        api_call_count += 1
        data = response.json()
        # print(data['results'])
        for ticker in data['results']:
            tickers.append(ticker)

    #print(len(tickers))

    example_ticker = {'ticker': 'BACpS',
     'name': 'Bank of America Corporation Depositary shares, each representing 1/1,000th interest in a share of 4.750% Non-Cumulative Preferred Stock, Series SS',
     'market': 'stocks',
     'locale': 'us',
     'primary_exchange': 'XNYS',
     'type': 'PFD',
     'active': True,
     'currency_name':
     'usd',
     'cik': '0000070858',
     'last_updated_utc': '2025-09-21T06:04:50.626926932Z'}

    # Write tickers to CSV with the same schema as example_ticker
    csv_filename = 'tickers.csv'
    fieldnames = list(example_ticker.keys())
    # mode = w => write mode
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t in tickers:
            # Ensure all fields are present, fill missing with ''
            row = {key: t.get(key, '') for key in fieldnames}
            writer.writerow(row)

    print(f'Wrote {len(tickers)} rows to {csv_filename}')

if __name__ == '__main__':
    run_stock_job()