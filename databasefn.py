import os
import psycopg2

class Database:

    TAKEAWAY_TIME_LIMIT = '00:07'
    DINE_IN_TIME_LIMIT = '00:25'
    DINE_IN_WARN_AMOUNT = 45
    TAKEAWAY_WARN_AMOUNT = 12

    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        self.cur = conn.cursor()

        self.cur.execute("CREATE TABLE t(id varchar(255), timelimit time, type int);")

    def purge(self):
        self.cur.execute("DELETE FROM t;")

    def addDineInUser(self,id):
        if (self.checkUser(id)):
            return False

        query = "INSERT INTO t(id,timelimit,type) VALUES('{}',current_time + time '{}',1);".format(id, self.DINE_IN_TIME_LIMIT)
        self.cur.execute(query)

        if (self.countDineInUser() == self.DINE_IN_WARN_AMOUNT):
            return True
        else:
            return False

    def addTakeAwayUser(self,id):
        if (self.checkUser(id)):
            return False

        query = "INSERT INTO t(id,timelimit,type) VALUES('{}',current_time + time '{}',2);".format(id, self.TAKEAWAY_TIME_LIMIT)
        self.cur.execute(query)

        if (self.countTakeAwayUser() == self.TAKEAWAY_WARN_AMOUNT):
            return True
        else:
            return False

    def remove(self,id):
        old_amount = self.getCount()

        query = "DELETE FROM t where id='{}';".format(id)
        self.cur.execute(query)

        new_amount = self.getCount()

        if (old_amount[0] - new_amount[0] == 1 and self.countTakeAwayUser() == self.DINE_IN_WARN_AMOUNT - 1):
            return 1
        elif (old_amount[1] - new_amount[1] == 1 and self.countTakeAwayUser() == self.TAKEAWAY_WARN_AMOUNT - 1):
            return 2
        else:
            return 0

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
