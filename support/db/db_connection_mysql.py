import pymysql.cursors
from settings import *


class DbConnectionMysql():
    @staticmethod
    def get_connection():
        connection = pymysql.connect(
            host=SRM_DB_HOST,
            user=SRM_DB_USERNAME,
            password=SRM_DB_PASSWORD,
            db=SRM_DB_NAME,
            port=int(SRM_DB_PORT),
            cursorclass=pymysql.cursors.DictCursor

        )
        connection.commit()
        return connection

    def get_data(self, sql):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        return row

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



