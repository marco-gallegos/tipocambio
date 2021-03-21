"""
@Author     Marco A. Gallegos Loaeza <ma_galeza@hotmail.com>
@Date       2021/03/12
@Updated    2021/03/12
@Description
    This file schedules the tc script to every day.
"""
import schedule
import time, pendulum
from crawler import *


def ok():
    url = "http://www.eldolar.info/es-MX/mexico/dia/hoy"
    pagina = Crawler(url)
    pagina.SetMaxTcInServer()


# schedule.every(2).seconds.do(ok)
schedule.every().day.at("08:50").do(ok)
schedule.every().day.at("09:00").do(ok)
schedule.every().day.at("09:10").do(ok)
schedule.every().day.at("09:20").do(ok)
schedule.every().day.at("09:30").do(ok)

while True:
    schedule.run_pending()
    time.sleep(seconnd=60*5)