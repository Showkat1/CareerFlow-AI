
import streamlit as st

from locations.location_data import (
    SPECIAL_LOCATIONS,
    get_cities,
    get_countries,
    get_regions,
)


def location_selector(initial_locations=None, key="cf_locations"):
    """Display cascading location dropdowns and manage selections."""

    selected_key = f"{key}_selected"

    if selected_key not in st.session_state:
        st.session_state[selected_key] = list(initial_locations or [])

    st.markdown("#### 🌍 Preferred locations")

    country = st.selectbox(
        "Country",
        ["Select a country"] + get_countries(),
        key=f"{key}_country",
    )

    region = "Select a region"
    city = "Select a city"

    if country != "Select a country":
        region = st.selectbox(
            "State / Region",
            ["Select a region"] + get_regions(country),
            key=f"{key}_region_{country}",
        )

        if region != "Select a region":
            city = st.selectbox(
                "City",
                ["Select a city"] + get_cities(country, region),
                key=f"{key}_city_{country}_{region}",
            )

    if st.button("＋ Add selected location", key=f"{key}_add"):
        location = None

        if city != "Select a city":
            location = f"{city}, {region}, {country}"
        elif region != "Select a region":
            location = f"{region}, {country}"
        elif country != "Select a country":
            location = country

        if location:
            current = st.session_state[selected_key]

            if location not in current:
                current.append(location)
                st.session_state[selected_key] = current
                st.rerun()
            else:
                st.info("This location is already selected.")
        else:
            st.info("Select a country, region, or city first.")

    special = st.selectbox(
        "Global work location",
        ["Select an option"] + SPECIAL_LOCATIONS,
        key=f"{key}_special",
    )

    if st.button("＋ Add global location", key=f"{key}_add_special"):
        if special != "Select an option":
            current = st.session_state[selected_key]

            if special not in current:
                current.append(special)
                st.session_state[selected_key] = current
                st.rerun()
            else:
                st.info("This location is already selected.")

    st.markdown("#### Selected locations")

    current = st.session_state[selected_key]

    updated = st.multiselect(
        "Deselect locations to remove them",
        options=current,
        default=current,
        key=f"{key}_editor",
    )

    st.session_state[selected_key] = updated

    return updated