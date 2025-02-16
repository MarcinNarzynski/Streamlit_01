import time

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
from streamlit.elements.lib.column_types import DateColumn, Column, LinkColumn, BarChartColumn, CheckboxColumn, ListColumn

from styles import get_status_color
from ui_components.gauge import plot_gauge

timer = time.time()

st.set_page_config(page_title="Night Tests", page_icon=":chart:", layout="wide")

st.title('Night Tests')
st.markdown("_Demo version 0.6_")
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


# https://unicode.org/emoji/charts/full-emoji-list.html
# PASSED = "\U0001F7E6"
PASSED = "\U0001F7E9"
# FAILED = "\U0001F534"
FAILED = "\U0001F534"

df_sorted = lib_test_statuses.sort_values('test_datetime', ascending=True)
df_sorted.drop(columns=['id'], inplace=True)
df_sorted["test_status_numeric"] = df_sorted.apply(lambda x: PASSED if x['test_status'] == "PASS" else FAILED, axis=1)

print(f"DB SORTED: \n{df_sorted}")

df_groupped_all = df_sorted.groupby(by='lib_name').agg(
    test_datetime=pd.NamedAgg(column="test_datetime", aggfunc="last"),
    test_status=pd.NamedAgg(column="test_status", aggfunc="last"),
    report_url=pd.NamedAgg(column="report_url", aggfunc="last"),
    test_history=pd.NamedAgg(column="test_status_numeric", aggfunc=lambda x: list(x)[:5]),
)

print(f"\nDB GROUPPED ALL: \n{df_groupped_all} \n{len(df_groupped_all)=}")


df_passed = df_groupped_all[df_groupped_all['test_status'] == 'PASS']
passed_count = df_passed.shape[0]

df_failed = df_groupped_all[df_groupped_all['test_status'] == 'FAIL']
failed_count = df_failed.shape[0]


df_columns = {
    "lib_name": Column("Library", width="medium"),
    "test_datetime": DateColumn("Date", format="DD-MMM", width="small"),
    "test_status": Column("Test Status", width="small"),
    "report_url": LinkColumn("Report URL", width="medium"),
    "test_history": ListColumn("Test History", width=None),
}
left_column, mid_column, right_column = st.columns((1,8,1))

with mid_column:
    plot_gauge(indicator_value=failed_count, indicator_color="red", indicator_title="Failed tests", max_bound=failed_count+passed_count)

    st.dataframe(df_groupped_all.style.apply(lambda x: x.map(get_status_color), axis=None),
                 column_config=df_columns,
                 use_container_width=True,
                 column_order=["lib_name", "test_status", "test_datetime", "report_url", "test_history"]
                 )

timer_end = time.time() - timer
dashboard_load_state.text(f"Refreshing dashboard done in {timer_end:.2f} seconds.")
