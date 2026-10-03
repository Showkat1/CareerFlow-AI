import streamlit as st

from locations.location_data import (
    get_countries,
    get_regions,
    get_cities,
)

st.set_page_config(
    page_title="Location Dropdown Diagnostic",
    layout="wide",
)

st.title("Location Dropdown Diagnostic")

country = st.selectbox(
    "Country",
    ["Select a country"] + get_countries(),
    key="diagnostic_country",
)

st.write("Selected country:", country)

if country != "Select a country":
    region = st.selectbox(
        "State / Region",
        ["Select a region"] + get_regions(country),
        key="diagnostic_region",
    )

    st.write("Selected region:", region)

    if region != "Select a region":
        city = st.selectbox(
            "City",
            ["Select a city"] + get_cities(country, region),
            key="diagnostic_city",
        )
        st.write("Selected city:", city)