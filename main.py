import time

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
from streamlit.elements.lib.column_types import DateColumn, Column, LinkColumn, BarChartColumn

from styles import get_status_color

timer = time.time()
st.title('Night Tests')
dashboard_load_state = st.text('Refreshing dashboard...')

db_url = "mysql+mysqlconnector://{USER}:{PWD}@{HOST}/{DBNAME}"
db_url = db_url.format(
    USER = "root",
    PWD = "1000",
    HOST = "localhost:3306",
    DBNAME = "marcin_db"
)

engine = create_engine(db_url, echo=False)

with engine.begin() as conn:
    lib_test_statuses = pd.read_sql_table(
        table_name='lib_night_tests',
        con=conn
    )


# sql_query = text("""select *
#                 from lib_night_tests
#                 # where test_status = 'PASS'
#                 # group by lib_name, test_datetime, test_status
#                 order by test_datetime desc
#                 """)

# with engine.begin() as conn:
#     all_tests = pd.read_sql_query(
#         sql=sql_query,
#         con=conn
#     )


df_sorted = lib_test_statuses.sort_values('test_datetime', ascending=False)
df_sorted.drop(columns=['id'], inplace=True)
df_sorted["test_status_numeric"] = df_sorted.apply(lambda x: 1 if x['test_status'] == "PASS" else 10, axis=1)

print(f"DB SORTED: \n{df_sorted}")




# df_groupped = df_sorted.groupby('lib_name').all()
#
# print(f"\nDB GROUPPED: \n{df_groupped}\n {len(df_groupped)=}")


df_groupped_first = df_sorted.groupby('lib_name').first()
# df_groupped_all = df_sorted.groupby(by='lib_name').agg({
#     "test_datetime": "first",
#     "test_status": "first",
#     "report_url": "first",
#     "test_status_numeric": "all"
# })

df_groupped_all = df_sorted.groupby(by='lib_name').agg(
    test_datetime=pd.NamedAgg(column="test_datetime", aggfunc="first"),
    test_status=pd.NamedAgg(column="test_status", aggfunc="first"),
    report_url=pd.NamedAgg(column="report_url", aggfunc="first"),
    test_history=pd.NamedAgg(column="test_status_numeric", aggfunc=lambda x: list(x)[:5]),
)

print(f"\nDB GROUPPED FIRST: \n{df_groupped_first} \n{len(df_groupped_first)=}")
print(f"\nDB GROUPPED ALL: \n{df_groupped_all} \n{len(df_groupped_all)=}")



# for lib in df_groupped_first["lib_name"].tolist():
#     mask = df_sorted["lib_name"] == lib
#     pos = np.flatnonzero(mask)
#     history = df_sorted.iloc[pos]["test_status_numeric"]
#     df_groupped_first["history"].apply(history)

# df_grouped_first["test_history"] = df_sorted.apply(lambda x: x['test_status_numeric'] if x['lib_name']==df_groupped_first['lib_name'], axis=1)

# print(f"\nDB GROUPPED FIRST: \n{df_groupped_first} \n{len(df_groupped_first)=}")
#
# df_passed = df_groupped_first[df_groupped_first['test_status'] == 'PASS']
# print(f"{len(df_passed)=}")
#
# df_failed = df_groupped_first[df_groupped_first['test_status'] == 'FAIL']
# print(f"{len(df_failed)=}")


columns = {
    "lib_name": Column("Library", width=200),
    "test_status": Column("Test Status", width=100),
    "test_datetime": DateColumn("Date", format="DD-MMM", width=100),
    "report_url": LinkColumn("Report URL", width=150),
    "test_history": BarChartColumn("Test History", width=100, y_min=0, y_max=11, styles={"color": "green"}),
}

st.dataframe(df_groupped_all.style.apply(lambda x: x.map(get_status_color), axis=None),
             column_config=columns,
             width=1000,
             # hide_index=True,
             )
# st.metric(label="Night test status",
#           )

timer_end = time.time() - timer
dashboard_load_state.text(f"Refreshing dashboard done in {timer_end:.2f} seconds.")


