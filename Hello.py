import streamlit as st
import duckdb

st.set_page_config(
    page_title="DuckDB",
    page_icon="👋",
)

st.write("# DuckDB is Awesome! 👋")


con = duckdb.connect('md:?motherduck_token=<token>')

# Query for filtered data
query = """
SELECT 
  *
FROM my_db.main.pokemon
"""
df = con.execute(query).df()

st.text(df.head())