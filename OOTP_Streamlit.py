import streamlit as st
import pandas as pd

# Load the Excel file from the URL
data_url = 'https://github.com/LeScott2406/OOTP/raw/refs/heads/main/MLB.xlsx'

# Read the data into a pandas DataFrame
df = pd.read_excel(data_url)

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

# Add the Player Type column based on the POS column
df['Player Type'] = df['POS'].apply(determine_player_type)

# Streamlit app
st.title("Baseball Player Stats Analyzer")

# Player Type selection
player_type = st.selectbox("Select Player Type", ["Pitcher", "Hitter"])

# Add the ORG filter with 'All' option
org_options = ['All'] + df['ORG'].unique().tolist()  # Add 'All' to the list of organizations
org_filter = st.selectbox("Select Organization", org_options)

# Filter the DataFrame based on Player Type
if player_type == "Pitcher":
    st.write("Pitcher Information:")
    pitcher_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'T', 'OVR', 'POT', 'WE', 'INT', 'G/F', 'VELO', 
                       'STM', 'Pitcher Current', 'Pitcher Potential', 'Pitch % Developed', '#50P', '#60P', '#70P']
    
    # Filter data to show only Pitchers
    pitcher_data = df[df['Player Type'] == 'Pitcher'][pitcher_columns]

    # Apply ORG filter if not 'All'
    if org_filter != 'All':
        pitcher_data = pitcher_data[pitcher_data['ORG'] == org_filter]

    st.write(pitcher_data)

elif player_type == "Hitter":
    st.write("Hitter Information:")
    hitter_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'B', 'T', 'OVR', 'POT', 'WE', 'INT', 'Hit Ability', 
                      'Hit Potential', 'Hit % Developed', 'Exit Velocity', 'EV Potential', 'Defence']
    
    # Filter data to show only Hitters
    hitter_data = df[df['Player Type'] == 'Hitter'][hitter_columns]

    # Apply ORG filter if not 'All'
    if org_filter != 'All':
        hitter_data = hitter_data[hitter_data['ORG'] == org_filter]

    st.write(hitter_data)
