import psycopg2
from settings import SRM_DB_PORT, SRM_DB_HOST, SRM_DB_NAME, SRM_DB_PASSWORD, SRM_DB_USERNAME


# class DbConnectionPostgre():
def connect():
    connection = psycopg2.connect(user=SRM_DB_USERNAME,
                                  password=SRM_DB_PASSWORD,
                                  host=SRM_DB_HOST,
                                  port=int(SRM_DB_PORT),
                                  database=SRM_DB_NAME)
    connection.commit()
    return connection


def get_data():
    db = connect()
    cursor = db.cursor()
    cursor.execute('select * from product_product where id = 2;')
    row = cursor.fetchone()
    print(row)


if __name__ == '__main__':
    get_data()
