"""
@Author     Marco A. Gallegos Loaeza <ma_galeza@hotmail.com>
@Date       2019/12/01
@Updated    2019/12/01
@Description
    legacy code
"""

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import datetime
import pendulum
from Server import *
from ORM import *

# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


class Crawler(object):
    """Se enfoca en resolver en automatico la comparacion entre los TC del dia"""

    def __init__(self, url):
        """Constructor for Crawler"""
        self.url = url

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
            nombre = nombre[1].text.upper()
            # print(nombre)
            if len(tds) == 5:
                # print(tds[4].contents[0])
                if nombre == "BANAMEX":
                    tiposdeCambio.append(tds[4].contents[0])
                if nombre.find("DOF") != -1:
                    tiposdeCambio.append(tds[4].contents[0])
            else:
                # print(tds[3].contents[0])
                if nombre == "BANAMEX":
                    tiposdeCambio.append(tds[3].contents[0])
                if nombre.find("DOF") != -1:
                    tiposdeCambio.append(tds[3].contents[0])

        tcMasAlto = max(tiposdeCambio)

        #print(tiposdeCambio)
        #print(tcMasAlto)
        return float(tcMasAlto)

    def SetMaxTcInServer(self):
        db = ORM_MYSQL()
        tc = tipocamb()
        tcAlto = self.GetMaxTc()
        fecha = pendulum.now().strftime("%Y-%m-%d")
        if tcAlto == 0:
            print("tipo de cambio es 0 no se inserta en db")
            return False

        # tipo de cambio de hoy
        # query = "Select * from tipocamb where fecha = '" + str(fecha) + "'"
        query = (tc.select().where(tipocamb.Fecha == str(fecha)))
        registro = None
        for row in query:
            print(row)
            registro = row

        if registro is None:
            #query = "insert into tipocamb(fecha, tipo_cambio) values('{0}',{1})"
            #tcStored = 0
            #query = query.format(fecha,tcAlto)
            #print(query)
            #db.execute(query)
            tipocamb.create(Fecha=fecha, Tipo_Cambio=tcAlto)
            print(f"se registro el tc {tcAlto}")
        else:
            """
            query = "update tipocamb set tipo_cambio = {0} where fecha = '{1}'"
            tcStored = float(registro[1])
            if tcStored < tcAlto:
                query = query.format(tcAlto,fecha)
                db.execute(query)
                log = Log()
                log.setup_db()

                tcAlto = self.GetMaxTc()
                fecha = datetime.today()
                fecha_log = fecha.strftime("%Y-%m-%d %H:%M:%S")
                fecha = fecha.strftime("%Y-%m-%d")
                if tcAlto is 0:
                    Log.create(tc=tcAlto, fecha=fecha_log, mensaje="Error al obtener tc")
                    return False

                # tipo de cambio de hoy
                fecha_actual_db_query = tipocamb.select().where(tipocamb.Fecha == fecha)
                # print(str(f"registros encontrados : {fecha_actual_db_query.count()}"))

                if fecha_actual_db_query.count() is 0:
                    # no hay asi que se registra lo obtenido
                    newTc = tipocamb.create(Fecha = fecha, Tipo_Cambio = tcAlto)
                    print(f"se guardo {newTc.Tipo_Cambio}")
                    Log.create(tc = tcAlto,fecha=fecha_log,mensaje="Nuevo Registro insertado")

                else:
                    # tenemos tc almacenado hay que comparar
                    tcStored = fecha_actual_db_query.get()
                    print(f"Tc Almacenado {tcStored.Tipo_Cambio}  {tcStored.Fecha} ")
                    if tcStored.Tipo_Cambio < tcAlto:
                        tcStored.Tipo_Cambio = tcAlto
                        tcStored.save()
                        Log.create(tc=tcStored.Tipo_Cambio, fecha=fecha_log, mensaje="Se actualizo el tc")
                        print("se actualizo el tc a : " + str(tcAlto))
                    else:
                        Log.create(tc=tcStored.Tipo_Cambio, fecha=fecha_log, mensaje="No Se actualia nada")
                        print("no se actualiza nada")
            """
            tcStored = registro.Tipo_Cambio
            if tcStored < tcAlto:
                tipocamb.update({tipocamb.Tipo_Cambio: tcAlto}) \
                    .where(tipocamb.Fecha == fecha).execute()
                print("se actualizo el tc a : " + str(tcAlto))
            else:
                print("no se actualiza nada")


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


if __name__ == "__main__":
    url = "http://www.eldolar.info/es-MX/mexico/dia/hoy"
    cr = Crawler(url)
    cr.SetMaxTcInServer()