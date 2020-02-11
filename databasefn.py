import os
import psycopg2

class Database:

    TAKEAWAY_TIME_LIMIT = '00:10'
    DINE_IN_TIME_LIMIT = '00:20'

    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        self.cur = conn.cursor()

        self.cur.execute("CREATE TABLE t(id varchar(255), timelimit time);")

    def purge(self):
        self.cur.execute("DELETE FROM t;")

    def addTakeAwayUser(self,id):
        query = "INSERT INTO t(id,timelimit) VALUES('{}',current_time + time '{}');".format(id, self.TAKEAWAY_TIME_LIMIT)
        self.cur.execute(query)

    def addDineInUser(self,id):
        query = "INSERT INTO t(id,timelimit) VALUES('{}',current_time + time '{}');".format(id, self.DINE_IN_TIME_LIMIT)
        self.cur.execute(query)

    def remove(self,id):
        query = "DELETE FROM t where id='{}';".format(id)
        self.cur.execute(query)

    def getCount(self):
        query = 'select count(*) from t;'
        self.cur.execute(query)
        res = self.cur.fetchone()
        return res[0]

    def checkUser(self,id):
        query = "select count(*) from t where id = '{}';".format(id);
        self.cur.execute(query)
        res = self.cur.fetchone()
        return res[0] >= 1

    def getLate(self):
        query = 'select id from t where timelimit < current_time;'
        self.cur.execute(query)
        res = self.cur.fetchall()
        return [item for t in res for item in t]
