#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd

# Function to load and preprocess the data
@st.cache_data
def load_and_prepare_data(url):
    # Read the Excel file from the URL
    df = pd.read_excel(url)

    # Define the function to categorize players based on position
    def determine_player_type(pos):
        pitcher_positions = ['SP', 'RP', 'CL']
        hitter_positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
        if pos in pitcher_positions:
            return 'Pitcher'
        elif pos in hitter_positions:
            return 'Hitter'
        else:
            return 'Unknown'

    # Add the Player Type column
    df['Player Type'] = df['POS'].apply(determine_player_type)

    return df

# Load data once
data_url = 'https://github.com/LeScott2406/OOTP/raw/refs/heads/main/draft.xlsx'
df = load_and_prepare_data(data_url)

# Streamlit app
st.title("All MLB Players")

# Sidebar for filters
with st.sidebar:
    # Player Type selection
    player_type = st.selectbox("Select Player Type", ["Pitcher", "Hitter"])

    # Age filter (Slider)
    age_filter = st.slider("Select Age Range", min_value=16, max_value=40, value=(16, 40))

    # Position filter (Multi-select based on Player Type)
    if player_type == "Pitcher":
        pos_options = ['SP', 'RP', 'CL']
    elif player_type == "Hitter":
        pos_options = ['C', '1B', '2B', '3B', 'SS', 'RF', 'CF', 'LF']

    pos_filter = st.multiselect("Select Position(s)", pos_options, default=pos_options)

# Filter the DataFrame based on Player Type
filtered_df = df[df['Player Type'] == player_type]

# Apply Age filter
filtered_df = filtered_df[filtered_df['Age'].between(age_filter[0], age_filter[1])]

# Apply POS filter based on selected positions
filtered_df = filtered_df[filtered_df['POS'].isin(pos_filter)]

# Display the filtered data
if player_type == "Pitcher":
    st.write("Pitcher Information:")
    pitcher_columns = ['POS', 'Name', 'Lev', 'Age', 'T', 'OVR', 'POT', 'WE', 'INT', 'G/F', 'VT', 
                       'STM', 'Pitcher Current', 'Pitcher Potential', 'Pitch % Developed', '#50P', '#60P', '#70P', 'DraftScore_Percentile', 'DraftTier']
    
    # Filter data to show only Pitchers
    pitcher_data = filtered_df[pitcher_columns]
    st.write(pitcher_data)

elif player_type == "Hitter":
    st.write("Hitter Information:")
    hitter_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'B', 'T', 'OVR', 'POT', 'WE', 'INT', 'Hit Ability', 
                      'Hit Potential', 'Hit % Developed', 'Exit Velocity', 'EV Potential', 'Defence', 'DraftScore_Percentile', 'DraftTier']
    
    # Filter data to show only Hitters
    hitter_data = filtered_df[hitter_columns]
    st.write(hitter_data)

