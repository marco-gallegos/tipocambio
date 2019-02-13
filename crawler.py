from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime
from Server import *


class Crawler(object):
    """Se enfoca en resolver en automatico la comparacion entre los TC del dia"""

    def __init__(self, url):
        """Constructor for Crawler"""
        self.url =url

    def simple_get(self,url):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None

    def is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    def GetMaxTc(self):
        tcMasAlto = 0
        respuesta = self.simple_get(self.url)


        archivoHTML = open("respuesta.html", "w")
        archivoHTML.write(str(respuesta))
        archivoHTML.close()

        rawHTML = open("respuesta.html").read()
        HTML = BeautifulSoup(rawHTML, 'html.parser')
        rows = HTML.select("#dllsTable > tbody > tr")
        # print(len(HTML.select("#dllsTable > tbody > tr")))

        tiposdeCambio = list()

        for row in rows:
            tds = row.find_all('td')
            nombre = tds[0].find_all('span')
            nombre = nombre[1].text
            nombre = nombre.upper()
            # print(nombre)
            if len(tds) is 5:
                # print(tds[4].contents[0])
                if nombre == "BANAMEX":
                    tiposdeCambio.append(tds[4].contents[0])
                if nombre.find("DOF") is not -1:
                    tiposdeCambio.append(tds[4].contents[0])
            else:
                # print(tds[3].contents[0])
                if nombre == "BANAMEX":
                    tiposdeCambio.append(tds[3].contents[0])
                if nombre.find("DOF") is not -1:
                    tiposdeCambio.append(tds[3].contents[0])

        tcMasAlto = max(tiposdeCambio)

        return float(tcMasAlto)

    def SetMaxTcInServer(self):
        servidor = Server("server.ini")
        tcAlto = self.GetMaxTc()
        fecha = datetime.today()
        fecha = fecha.strftime("%Y-%m-%d")
        if tcAlto is 0:
            return False
        conexion = servidor.getConection()
        if conexion is False:
            return False
        db = conexion.cursor()

        query = "Select * from tipocamb where fecha = '" + str(fecha) + "'"

        db.execute(query)

        registro = db.fetchone()


        if registro is None:
            query = "insert into tipocamb(fecha, tipo_cambio) values('{0}',{1})"
            tcStored = 0
            query = query.format(fecha,tcAlto)
            print(query)
            db.execute(query)
            print("se registro el tc")
        else:
            query = "update tipocamb set tipo_cambio = {0} where fecha = '{1}'"
            tcStored = float(registro[1])
            if tcStored < tcAlto:
                query = query.format(tcAlto,fecha)
                db.execute(query)
                print("se actualizo el tc a : " + str(tcAlto))
            else:
                print("no se actualiza nada")

        print("tc almacenado : " + str(tcStored))

        conexion.close()
        print(fecha)

def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)