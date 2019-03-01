import pymysql.cursors
from dingdian import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_DB = settings.MYSQL_DB

cnx = pymysql.Connect(host=MYSQL_HOSTS,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB)
cur = cnx.cursor()

class Sql:
    @classmethod
    def insert_dd_name(cls,xs_name,xs_author,category,name_id):
        sql = "INSERT INTO dd_name VALUES (%(xs_name)s,%(xs_author)s,%(category)s,%(name_id)s)"
        value = (xs_name,xs_author,category,name_id)
        cur.execute(sql,value)
        cnx.commit()

    @classmethod
    def select_name(cls,name_id):
        sql = "SELECT EXISTS(SELECT 1 FROM dd_name WHERE name_id=%(name_id)s)"
        value = name_id
        cur.execute(sql,value)
        return cur.fetchall()[0]

