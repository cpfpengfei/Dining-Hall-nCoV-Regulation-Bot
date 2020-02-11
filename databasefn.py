import os
import psycopg2

class Database:

    TAKEAWAY_TIME_LIMIT = '00:07'
    DINE_IN_TIME_LIMIT = '00:25'

    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        self.cur = conn.cursor()

        self.cur.execute("CREATE TABLE t(id varchar(255), timelimit time, type int);")

    def purge(self):
        self.cur.execute("DELETE FROM t;")

    def addDineInUser(self,id):
        query = "INSERT INTO t(id,timelimit,type) VALUES('{}',current_time + time '{}',1);".format(id, self.DINE_IN_TIME_LIMIT)
        self.cur.execute(query)

    def addTakeAwayUser(self,id):
        query = "INSERT INTO t(id,timelimit,type) VALUES('{}',current_time + time '{}',2);".format(id, self.TAKEAWAY_TIME_LIMIT)
        self.cur.execute(query)

    def remove(self,id):
        query = "DELETE FROM t where id='{}';".format(id)
        self.cur.execute(query)

    def countDineInUser(self):
        query = 'select count(*) from t where type = 1;'
        self.cur.execute(query)
        res = self.cur.fetchone()
        return res[0]

    def countTakeAwayUser(self):
        query = 'select count(*) from t where type = 2;'
        self.cur.execute(query)
        res = self.cur.fetchone()
        return res[0]

    def getCount(self):
        return self.countDineInUser(), self.countTakeAwayUser()

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
