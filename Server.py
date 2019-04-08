from peewee import *
from datetime import *

class INI(object):
    def __init__(self, iniFile="server.ini"):
        self.iniFile = iniFile
        archivo = open(self.iniFile, "r")
        info = archivo.readline()
        info = info.split(",")
        self.db = info[0]
        self.ip = info[1]
        self.port = int(info[2])
        self.user = info[3]
        self.password = info[4]
        archivo.close()
    def __str__(self):
        return str(f"db : {self.db}\tip : {self.ip}\tport: {str(self.port)}\tuser : {self.user}\tpass : {self.password}")


# conexion a la db
configuracion = INI()
#print(str(configuracion))
mysql_db = MySQLDatabase(database=configuracion.db, user=configuracion.user, password=configuracion.password,
                         host=configuracion.ip, port=configuracion.port)


# clase abstracta
class ORM_MYSQL(Model):
    class Meta:
        database = mysql_db

    def test_conexion(self):
        status = True
        try:
            mysql_db.connect()
        except:
            status = False
        return status


# modelo para tc
class tipocamb(ORM_MYSQL):
    Fecha = DateField(primary_key=True)
    Tipo_Cambio = DoubleField()


if __name__ == "__main__":
    db = ORM_MYSQL()
    res = db.test_conexion()
    print(res)
    if res:
        print("ok")
    else:
        print("not ok")
    query = tipocamb.select()

    # for row in query:
    #    print(f"fecha : {str(row.Fecha)}\ttc : {str(row.)}")