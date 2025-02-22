import pandas as pd
from sqlalchemy import create_engine, Connection

connection: Connection | None = None

def initialize_db_connection() -> None:
    global connection

    db_url = "mysql+mysqlconnector://{USER}:{PWD}@{HOST}/{DBNAME}"
    db_url = db_url.format(
        USER = "root",
        PWD = "1000",
        HOST = "localhost:3306",
        DBNAME = "marcin_db"
    )

    if connection is None:
        engine = create_engine(db_url, echo=False)
        connection = engine.connect()
        print("Connection to database established successfully.")
        return

    print("Connection to database already established. Skipping.")


def read_table_from_db(table_name: str) -> pd.DataFrame | None:
    if connection:
        with connection.begin():
            result = pd.read_sql_table(table_name, connection)

        return result

    print("Connection to database must be established first. Skipping.")
