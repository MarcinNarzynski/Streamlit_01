import time

import pandas as pd
import streamlit as st
from streamlit import container
from streamlit.elements.lib.column_types import DateColumn, Column, LinkColumn, ListColumn
from streamlit_extras.bottom_container import bottom

import db_operations
from styles import get_status_color
from ui_components.gauge import plot_gauge

# To run type in command line: streamlit run main.py

timer = time.time()

st.set_page_config(page_title="Night Tests", page_icon=":chart:", layout="wide")

st.title('Night Tests', )
left_column, mid_column, right_column = st.columns((1,8,1))
bottom_left_column, bottom_mid_column, bottom_right_column = st.columns((1,8,1))
with mid_column:
    with st.container(border=True):
        st.markdown("_Demo version 0.6_")


db_operations.initialize_db_connection()
lib_test_statuses = db_operations.read_table_from_db("lib_night_tests")

# db_operations_alchemy.initialize_db_connection()
# lib_test_statuses = db_operations_alchemy.read_table_from_db("lib_night_tests")


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

with mid_column:
    with container(border=True):
        plot_gauge(indicator_value=failed_count, indicator_color="red", indicator_title="Failed tests", max_bound=failed_count+passed_count)

        st.dataframe(df_groupped_all.style.apply(lambda x: x.map(get_status_color), axis=None),
                     column_config=df_columns,
                     use_container_width=True,
                     column_order=["lib_name", "test_status", "test_datetime", "report_url", "test_history"]
                     )

with bottom():
    bottom_messages = st.text('Refreshing dashboard...')

timer_end = time.time() - timer
bottom_messages.text(f"Refreshing dashboard done in {timer_end:.2f} seconds.")
