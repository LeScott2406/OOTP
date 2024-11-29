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

# Player Type selection
player_type = st.selectbox("Select Player Type", ["Pitcher", "Hitter"])

# Filter the DataFrame based on Player Type
if player_type == "Pitcher":
    st.write("Pitcher Information:")
    pitcher_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'T', 'OVR', 'POT', 'WE', 'INT', 'G/F', 'VELO', 
                       'STM', 'Pitcher Current', 'Pitcher Potential', 'Pitch % Developed', '#50P', '#60P', '#70P']
    
    # Filter data to show only Pitchers
    pitcher_data = df[df['Player Type'] == 'Pitcher'][pitcher_columns]
    st.write(pitcher_data)

elif player_type == "Hitter":
    st.write("Hitter Information:")
    hitter_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'B', 'T', 'OVR', 'POT', 'WE', 'INT', 'Hit Ability', 
                      'Hit Potential', 'Hit % Developed', 'Exit Velocity', 'EV Potential']
    
    # Filter data to show only Hitters
    hitter_data = df[df['Player Type'] == 'Hitter'][hitter_columns]
    st.write(hitter_data)
