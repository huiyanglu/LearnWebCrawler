import pymysql.cursors
#from dingdianxs import settings

cnx = pymysql.Connect(host='localhost',
                        port=3306,
                        user='root',
                        password='87869973lhy',
                        database='mzitu')
cur = cnx.cursor()

"""SQL文件需要修改，按照教程的code是能保存到MySQL里的"""
class Sql:

    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        sql = 'INSERT INTO dd_name (`xs_name`, `xs_author`, `category`, `name_id`) VALUES (%(xs_name)s, %(xs_author)s, %(category)s, %(name_id)s)'
        value = {
            'xs_name': xs_name,
            'xs_author': xs_author,
            'category': category,
            'name_id': name_id
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_name(cls, name_id):
        sql = "SELECT EXISTS(SELECT 1 FROM dd_name WHERE name_id=%(name_id)s)"
        value = {
            'name_id': name_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def insert_dd_chaptername(cls, xs_chaptername, xs_content, id_name, num_id, url):
        sql = 'INSERT INTO dd_chaptername (`xs_chaptername`, `xs_content`, `id_name`, `num_id`, `url`) \
                VALUES (%(xs_chaptername)s, %(xs_content)s, %(id_name)s, %(num_id)s, %(url)s)'
        value = {
            'xs_chaptername': xs_chaptername,
            'xs_content': xs_content,
            'id_name': id_name,
            'num_id': num_id,
            'url': url
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_chapter(cls, url):
        sql = "SELECT EXISTS(SELECT 1 FROM dd_chaptername WHERE url=%(url)s)"
        value = {'url': url}
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def id_name(cls,xs_name):
        sql = 'SELECT id from dd_name WHERE xs_name=%(xs_name)s'
        value = {'xs_name':xs_name}
        cur.execute(sql, value)
        for name_id in cur:
            return name_id[0]

