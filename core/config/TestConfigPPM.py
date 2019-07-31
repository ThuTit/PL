from core.db.db_connection import DbConnection
from core.db.sql_script import insert_promotion_warning


class TestConfigPPM(DbConnection):

    def setup_class(self):
        DbConnection.execute_query(self, insert_promotion_warning)

    def teardown_class(self):
        DbConnection.close_db(self)
