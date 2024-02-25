import streamlit as st
import duckdb
import pandas as pd
import altair as alt

# Set Streamlit page configuration
st.set_page_config(
    page_title="PokeData",
    page_icon="📊",
)

# Welcome message
st.markdown(
    """
        # Welcome to PokéData! 👋

        *The #1 place to explore Pokémon data!*
    """
)


# Connect to DuckDB database
con = duckdb.connect("md:?motherduck_token=" + st.secrets["motherduck_token"])


# Query for filtered data
query = """
SELECT 
  *
FROM my_db.main.pokemon
"""
pokemon_df = con.execute(query).df()


# Rename the '_name' column to 'Pokemon' and 'height' to 'Height' in the DataFrame
pokemon_df.rename(columns={'_name': 'Pokemon', 'height': 'Height'}, inplace=True)


# Sort the DataFrame by height in descending order and select the top 10 tallest Pokémon
top_10_tallest = pokemon_df.nlargest(10, 'Height')


# Streamlit Divider
st.divider()


##########################################################################################
# Streamlit Header for Bar Chart
##########################################################################################

st.write("## The Height of the Top 10 Tallest Pokémon! 📏")


##########################################################################################
# Altair Charts
##########################################################################################

# Create Altair chart for images
image_chart = alt.Chart(top_10_tallest, height=500).mark_image(
    width=35,
    height=35
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
combined_chart = alt.layer(bar_chart, image_chart).configure_axis(
    grid=False
)


# Display the combined chart using Streamlit
st.altair_chart(combined_chart, use_container_width=True)
