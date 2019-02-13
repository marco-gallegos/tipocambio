import MySQLdb

class Server(object):
    """Instancia de un servidor apartir de un archivo de configuracion ini"""

    def __init__(self, iniFile):
        """Constructor for Server"""
        self.iniFile = iniFile
        self.db = None
        self.ip = None
        self.port = None
        self.user = None
        self.password = None
        self.GetIni()

    def GetIni(self):
        archivo = open(self.iniFile,"r")
        info = archivo.readline()
        info = info.split(",")
        self.db = info[0]
        self.ip = info[1]
        self.port = info[2]
        self.user = info[3]
        self.password = info[4]
        archivo.close()

    def testConection(self):
        conexion = MySQLdb.connect(host = self.ip, port=int(self.port), db=self.db, user = self.user,
                                   password = self.password)

        if conexion:
            return True
        else:
            return False

        conexion.close()

    def getConection(self):
        conexion = MySQLdb.connect(host=self.ip, port=int(self.port), db=self.db, user=self.user,
                                   password=self.password)
        if conexion:
            return conexion
        else:
            return False

    def __str__(self):
        cadena  = "Servidor :\t" + str(self.ip) + "\n"
        cadena += "DB       :\t" + str(self.db) + "\n"
        cadena += "Puerto   :\t" + str(self.port) + "\n"
        cadena += "Conexion :\t" + str(self.testConection()) + "\n"
        return cadena