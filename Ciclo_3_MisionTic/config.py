class dev():
    DEBUG=True
    SECRECT_KEY=""
    DATABASE={
        'name':'db.sqlite3',
        'engine':'peewee.SqliteDatabase'
    }

class pro():
    DEBUG=False
    SECRECT_KEY=""
    DATABASE={
        'name':'db.sqlite3',
        'engine':'peewee.SqliteDatabase',
        'host':'ur.db.com',
        'user':'prueba',
        'password':'prueba'
    }