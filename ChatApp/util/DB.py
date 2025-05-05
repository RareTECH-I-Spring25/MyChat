import os
import pymysql
from pymysqlpool.pool import Pool

class DB:
    @staticmethod
    def init_db_pool():
        pool = Pool(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            db=os.environ.get('DB_DATABASE', 'mychat'),
            autocommit=True
        )
        pool.init()
        return pool 