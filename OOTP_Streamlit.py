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

# Sidebar Filters
with st.sidebar:
    # Player Type selection
    player_type = st.selectbox("Select Player Type", ["Pitcher", "Hitter"])
    
    # Filter by ORG (Organization)
    org_options = df['ORG'].unique().tolist()
    org_filter = st.selectbox("Select Organization", org_options)
    
    # Filter by Age
    age_filter = st.slider("Select Age Range", min_value=16, max_value=40, value=(16, 40))

# Filter the DataFrame based on Player Type
filtered_df = df[df['Player Type'] == player_type]

# Apply the ORG filter if it is not "All"
if org_filter:
    filtered_df = filtered_df[filtered_df['ORG'] == org_filter]

# Apply the Age filter
filtered_df = filtered_df[filtered_df['Age'].between(age_filter[0], age_filter[1])]

# Filtered data display
if player_type == "Pitcher":
    st.write("Pitcher Information:")
    pitcher_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'T', 'OVR', 'POT', 'WE', 'INT', 'G/F', 'VELO', 
                       'STM', 'Pitcher Current', 'Pitcher Potential', 'Pitch % Developed', '#50P', '#60P', '#70P']
    
    pitcher_data = filtered_df[pitcher_columns]
    st.write(pitcher_data)

elif player_type == "Hitter":
    st.write("Hitter Information:")
    hitter_columns = ['POS', 'Name', 'ORG', 'Lev', 'Age', 'B', 'T', 'OVR', 'POT', 'WE', 'INT', 'Hit Ability', 
                      'Hit Potential', 'Hit % Developed', 'Exit Velocity', 'EV Potential', 'Defence']
    
    hitter_data = filtered_df[hitter_columns]
    st.write(hitter_data)
