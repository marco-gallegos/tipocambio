"""
@Author     Marco A. Gallegos Loaeza <ma_galeza@hotmail.com>
@Date       2019/12/01
@Updated    2019/12/01
@Description
    legacy code
"""
from crawler import *

url = "http://www.eldolar.info/es-MX/mexico/dia/hoy"
pagina = Crawler(url)
pagina.SetMaxTcInServer()