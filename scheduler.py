import schedule
import time
from script import run_stock_job # importing it from different file

from datetime import datetime

def basic_job():
    print("Job started at:", datetime.now())

# Run every minute
schedule.every().minute.do(basic_job)

# 9AM is based on the timezone set in your system. On the cloud, it will be based on UTC
#schedule.every().day.at("09:00").do(run_stock_job())

# Run every minute
schedule.every().minute.do(run_stock_job)

while True:
    schedule.run_pending()
    time.sleep(1)


# problems with schedulers like this:
# What if you close your laptop, it will stop running
# You need crons running in a background process
# Can use crontab to schedule thing in the background.
# Use https://crontab.guru/ to determine the best expression touse for your job
# can also use @daily -> same as 0 0 * * *
# minute hour day(month) month day(week)
# utility called 'crontab -e' to edit the cron jobs
# find path using pwd and then add cron to it as follows
# * * * * * /usr/bin/python3 ~/Documents/data-engineering-bootcamp/stock-trading-python-app
# Schedulers like Airflow also uses cron expressions to schedule jobs