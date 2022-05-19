# streamlit_app.py

import streamlit as st
import mysql.connector
import pandas as pd

st.title('FFXI Omega Server GM Audit')
st.caption('If you see something, SAY SOMETHING!')

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from audit_gm;")
date_time = []
gm_name = []
gm_command = []
full_command = []

# Print results.
for row in rows:
    date_time.append(row[0])
    gm_name.append(row[1])
    gm_command.append(row[2])
    full_command.append(row[3])

df_date = pd.DataFrame({'Date/Time':date_time})
df_gm_name = pd.DataFrame({'GM Name':gm_name})
df_gm_command = pd.DataFrame({'Command':gm_command})
df_full_command = pd.DataFrame({'Full Command':full_command})                


master_df = pd.concat(
        [df_date, df_gm_name, df_gm_command, df_full_command], axis=1, join="inner")
master_df_style =  master_df.style.set_table_styles([
                            {
                                "selector":"thead",
                                "props": [("background-color", "#2a9d8fff"), ("color", "white"),
                                          ("border", "3px solid white"),
                                          ("font-size", "1rem"), ("font-weight:", "bold")]
                            },
                            {
                                "selector":"th.row_heading",
                                "props": [("background-color", "#2a9d8fff"), ("color", "white"),
                                          ("border", "3px solid white"),
                                          ("font-size", "1rem"), ("font-style", "italic")]
                            },
                            {
                                "selector":"th.col_heading",
                                "props": [("color", "white"),
                                          ("border", "3px solid white"),
                                          ("font-size", "1rem"), ("font-weight:", "bold")]
                            }
                        ])        
st.dataframe(master_df_style)