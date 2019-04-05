from peewee import *

sqlite_db = SqliteDatabase('optimizacion.db',
    pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class ORM_LOG(Model):
    """Modelo base para que use nuestra instancia de peewee."""
    class Meta:
        database = sqlite_db

    def setup_db(self):
        sqlite_db.connect()
        sqlite_db.create_tables([log])
        sqlite_db.close()


class log(ORM_LOG):
    time = DateTimeField()
    tc = FloatField()


if __name__ == "__main__":
    orm = ORM_LOG()
    orm.setup_db()