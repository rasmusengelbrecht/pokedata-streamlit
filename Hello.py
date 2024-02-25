import streamlit as st
import duckdb
import pandas as pd
import altair as alt

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
pokemon_df = con.execute(query).df()

# Rename the '_name' column to 'pokemon' in the DataFrame
pokemon_df.rename(columns={'_name': 'Pokemon','height': 'Height'}, inplace=True)

# Sort the DataFrame by height in descending order and select the top 10 tallest Pokémon
top_10_tallest = pokemon_df.nlargest(10, 'Height')



# st.data_editor(
#     top_10_tallest,
#     column_config={
#         "sprite_url": st.column_config.ImageColumn(
#             "Preview Image", help="Streamlit app preview screenshots"
#         )
#     },
#     column_order=["sprite_url", "Height"],
#     hide_index=True,
# )

st.divider()

st.write("## The Height of the Top 10 Tallest Pokémon! 📏")

# Create Altair chart for images
image_chart = alt.Chart(top_10_tallest, height=500).mark_image(
    width=40,
    height=40
).encode(
    x=alt.X('Pokemon', sort=None),  # Disable sorting to maintain original order
    y='Height',
    url='sprite_url'
)

# Create Altair chart for bars
bar_chart = alt.Chart(top_10_tallest, height=500).mark_bar(
    color='dimgrey'
).encode(
    x=alt.X('Pokemon', sort=None),  # Disable sorting to maintain original order
    y='Height'
)

# Layer the image chart and bar chart
combined_chart = alt.layer(bar_chart, image_chart)

st.altair_chart(combined_chart, use_container_width=True)