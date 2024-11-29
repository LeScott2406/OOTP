#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

# Caching function to load the data only once
@st.cache_data
def load_data():
    # Load the Excel file from the URL
    data_url = 'https://github.com/LeScott2406/OOTP/raw/refs/heads/main/MLB.xlsx'
    # Read the data into a pandas DataFrame
    return pd.read_excel(data_url)

# Load the data (this will be cached)
df = load_data()

# Define the function to categorize players based on position
def determine_player_type(pos):
    pitcher_positions = ['SP', 'RP', 'CL']
    hitter_positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH']
    if pos in pitcher_positions:
        return 'Pitcher'
    elif pos in hitter_positions:
        return 'Hitter'
    else:
        return 'Unknown'

# Add the Player Type column based on the POS column
df['Player Type'] = df['POS'].apply(determine_player_type)

# Streamlit app
st.title("Baseball Player Stats Analyzer")

# Create the sidebar for the filters (left side)
with st.sidebar:
    # Player Type selection
    player_type = st.selectbox("Select Player Type", ["Pitcher", "Hitter"])

    # Filter by ORG (Organization)
    org_options = ['All'] + df['ORG'].unique().tolist()
    org_filter = st.selectbox("Select Organization", org_options)

    # Filter by Age
    age_filter = st.slider("Select Age Range", min_value=16, max_value=40, value=(16, 40))

    # Filter by POS (Position)
    pos_options = ['All'] + df['POS'].unique().tolist()
    pos_filter = st.selectbox("Select Position", pos_options)

# Filter the DataFrame based on Player Type
filtered_df = df[df['Player Type'] == player_type]

# Apply filters based on ORG, Age, and POS
if org_filter != 'All':
    filtered_df = filtered_df[filtered_df['ORG'] == org_filter]

filtered_df = filtered_df[filtered_df['Age'].between(age_filter[0], age_filter[1])]

if pos_filter != 'All':
    filtered_df = filtered_df[filtered_df['POS'] == pos_filter]

# Display the filtered data
if player_type == "Pitcher":
    st.write("Pitcher Information:")
    pitcher_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'T', 'OVR', 'POT', 'WE', 'INT', 'G/F', 'VELO', 
                       'STM', 'Pitcher Current', 'Pitcher Potential', 'Pitch % Developed', '#50P', '#60P', '#70P']
    
    pitcher_data = filtered_df[pitcher_columns]
    st.dataframe(pitcher_data, use_container_width=True)  # Expands the table to fit the container width

elif player_type == "Hitter":
    st.write("Hitter Information:")
    hitter_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'B', 'T', 'OVR', 'POT', 'WE', 'INT', 'Hit Ability', 
                      'Hit Potential', 'Hit % Developed', 'Exit Velocity', 'EV Potential', 'Defence]
    
    hitter_data = filtered_df[hitter_columns]
    st.dataframe(hitter_data, use_container_width=True)  # Expands the table to fit the container width
