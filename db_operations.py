import pandas as pd
import pymysql
from pymysql import Connection

connection: Connection | None = None

def initialize_db_connection() -> None:
    global connection
    user = "root"
    pwd = "1000"
    host = "localhost"
    port = 3306
    dbname = "marcin_db"

    if connection is None:
        connection = pymysql.connect(host=host, user=user, password=pwd, db=dbname, port=port)
        print("Connection to database established successfully.")
        return

    print("Connection to database already established. Skipping.")


def read_table_from_db(table_name: str) -> pd.DataFrame | None:
    if connection:
        result = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
        return result

    print("Connection to database must be established first. Skipping.")
