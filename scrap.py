from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

respuesta = simple_get("http://www.eldolar.info/es-MX/mexico/dia/hoy");

archivoHTML = open("respuesta.html","w")
archivoHTML.write(str(respuesta))
archivoHTML.close()

rawHTML = open("respuesta.html").read()
HTML = BeautifulSoup(rawHTML, 'html.parser')
rows = HTML.select("#dllsTable > tbody > tr")
#print(len(HTML.select("#dllsTable > tbody > tr")))

tiposdeCambio = list()

archivoLog = open("diario.log","a")

for row in rows:
    tds = row.find_all('td')
    nombre = tds[0].find_all('span')
    nombre = nombre[1].text
    nombre = nombre.upper()
    #print(nombre)
    if len(tds) is 5:
        #print(tds[4].contents[0])
        if nombre == "BANAMEX" :
            archivoLog.write("BANAMEX ")
            archivoLog.write(tds[4].contents[0])
            archivoLog.write(" ,")

            tiposdeCambio.append(tds[4].contents[0])
        if nombre.find("DOF") is not -1 :
            archivoLog.write("DOF ")
            archivoLog.write(tds[4].contents[0])
            archivoLog.write(" ,")

            tiposdeCambio.append(tds[4].contents[0])
    else:
        #print(tds[3].contents[0])
        if nombre == "BANAMEX":
            archivoLog.write("BANAMEX ")
            archivoLog.write(tds[3].contents[0])
            archivoLog.write(" ,")

            tiposdeCambio.append(tds[3].contents[0])
        if nombre.find("DOF") is not -1:
            archivoLog.write("DOF ")
            archivoLog.write(tds[3].contents[0])
            archivoLog.write(" ,")

            tiposdeCambio.append(tds[3].contents[0])

#print("El mas alto es : " + str( max(tiposdeCambio) ))
#print(tiposdeCambio)
print("el tipo de cambio mas grande es " + str( max(tiposdeCambio) ) )

archivoLog.write("el tipo de cambio mas grande es " + str( max(tiposdeCambio) ) )

fecha = datetime.now()

archivoLog.write(", " + str( fecha ) + ",\n" )


archivoLog.close()