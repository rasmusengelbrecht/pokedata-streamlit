import streamlit as st
import duckdb

st.set_page_config(
    page_title="PokeData",
    page_icon="📊",
)

st.write("# Welcome to PokéData! 👋")

con = duckdb.connect("md:?motherduck_token=" + st.secrets["motherduck_token"])

# Query for filtered data
query = """
SELECT 
  *
FROM my_db.main.pokemon
"""
df = con.execute(query).df()

st.text(df)

