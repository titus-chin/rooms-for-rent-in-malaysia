import pandas as pd
import streamlit as st
from datetime import date


@st.cache
def load_data(date):
    data = pd.read_csv("data/malaysia_rental_lists.csv")
    data.sort_values(["Area", "Rent (RM/month)", "Location"], inplace=True)
    data.set_index("Area", drop=True, inplace=True)
    return data


@st.cache
def get_location_options(data, area, date):
    try:
        location = data.loc[area, "Location"].unique()
    except:
        location = [data.loc[area, "Location"]]
    return location


@st.cache
def select_data(data, area, location, date):
    selected_data = data.loc[area]
    try:
        selected_data = selected_data[selected_data["Location"].isin(location)]
    except:
        selected_data = pd.DataFrame(
            {
                "Location": location,
                "Rent (RM/month)": selected_data.values[1],
                "Headline": selected_data.values[2],
                "Link": selected_data.values[3],
            }
        )
    return selected_data


st.title("Rooms for Rent in Malaysia")
today_date = date.today()
st.write(f"Updated at {today_date}")
data_load_state = st.text("Loading data...")
data = load_data(today_date)

area = st.sidebar.radio("Select area:", options=set(data.index), index=0)
location = st.sidebar.multiselect(
    "Select location:",
    options=get_location_options(data, area, today_date),
    default=get_location_options(data, area, today_date)[0],
)
selected_data = select_data(data, area, location, today_date)
st.write(
    selected_data.to_html(escape=False, index=False, render_links=True),
    unsafe_allow_html=True,
)
data_load_state.text("Loading data...done!")
