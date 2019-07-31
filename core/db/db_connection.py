import pymysql.cursors
from settings import *


class DbConnection():
    @staticmethod
    def get_connection():
        connection = pymysql.connect(
            host=PPM_DB_HOST,
            user=PPM_DB_USERNAME,
            password=PPM_DB_PASSWORD,
            db=PPM_DB_NAME,
            port=3313,
            cursorclass=pymysql.cursors.DictCursor

        )
        connection.commit()
        return connection

    # def get_data(self, sql):
    #     db = self.get_connection()
    #     cursor = db.cursor()
    #     cursor.execute(sql)
    #     row = cursor.fetchone()
    #     return row

    def execute_query(self, sql):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return
    def close_db(self):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.close()



