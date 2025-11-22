#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

# Function to load and preprocess the data
@st.cache_data
def load_and_prepare_data(url):
    # Read the Excel file from the URL
    df = pd.read_excel(url)
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces

    # Function to categorize players based on position
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

# Initialize session state for drafted players
if 'drafted' not in st.session_state:
    st.session_state.drafted = set()  # store drafted player names

# Streamlit app
st.title("MLB Classic Draft")

# Sidebar for filters
with st.sidebar:
    player_type = st.selectbox("Select Player Type", ["Pitcher", "Hitter"])
    age_filter = st.slider("Select Age Range", min_value=16, max_value=40, value=(16, 40))

    if player_type == "Pitcher":
        pos_options = ['SP', 'RP', 'CL']
    else:
        pos_options = ['C', '1B', '2B', '3B', 'SS', 'RF', 'CF', 'LF']

    pos_filter = st.multiselect("Select Position(s)", pos_options, default=pos_options)

# Filter the DataFrame based on Player Type and filters
filtered_df = df[df['Player Type'] == player_type]
filtered_df = filtered_df[filtered_df['Age'].between(age_filter[0], age_filter[1])]
filtered_df = filtered_df[filtered_df['POS'].isin(pos_filter)]

# Columns to display
if player_type == "Pitcher":
    display_columns = ['POS', 'Name', 'Age', 'T', 'OVR', 'POT', 'WE', 'INT', 'G/F', 'VT',
                       'STM', 'Pitcher Current Norm', 'Pitcher Potential Norm', 'Pitch % Developed',
                       '#50P', '#60P', '#70P', 'DraftScore_Percentile', 'Tier']
else:
    display_columns = ['POS', 'Name', 'Age', 'B', 'T', 'OVR', 'POT', 'WE', 'INT',
                       'Hit Ability Norm', 'Hit Potential Norm', 'Hit % Developed',
                       'Exit Velocity Norm', 'EV Potential Norm', 'Defence Norm',
                       'DraftScore_Percentile', 'Tier']

# Keep only existing columns
display_columns = [col for col in display_columns if col in filtered_df.columns]
filtered_df = filtered_df[display_columns]

# Function to highlight drafted players
def highlight_drafted(row):
    if row['Name'] in st.session_state.drafted:
        return ['background-color: red'] * len(row)
    return [''] * len(row)

# Display main player table with highlighting
st.write("### Player Table")
st.dataframe(filtered_df.style.apply(highlight_drafted, axis=1))

# Draft buttons for each player
st.write("### Draft Players")
for i, row in filtered_df.iterrows():
    player_name = row['Name']
    drafted = player_name in st.session_state.drafted

    col1, col2 = st.columns([8, 1])
    with col1:
        # Show all player stats
        st.write(row.to_dict())
    with col2:
        if not drafted and st.button("Draft", key=f"draft_{i}"):
            st.session_state.drafted.add(player_name)
