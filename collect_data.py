print("Starting data collection...")

# Statbotics API
import statbotics
sb = statbotics.Statbotics()

# Blue Alliance API
TBA_API_KEY = "YOUR_TBA_API_KEY_HERE"
TBA_BASE_URL = "https://www.thebluealliance.com/api/v3"

import requests
# Fetch data for the same team using TBA
headers = {"X-TBA-Auth-Key": TBA_API_KEY}

print("Importing list_of_teams.csv...")

# Import list_of_teams.csv (this csv was hand-crafted)
import pandas as pd
teams_df = pd.read_csv("list_of_teams.csv")

print("Collecting team data from TBA and Statbotics APIs...")

# Add nickname and country columns to teams_df using TBA API
nicknames = []
countries = []

for _, row in teams_df.iterrows():
    team_number = row['team_nr']
    response = requests.get(f"{TBA_BASE_URL}/team/frc{team_number}", headers=headers)
    
    if response.status_code == 200:
        team_data = response.json()
        nicknames.append(team_data.get('nickname', 'Unknown'))
        countries.append(team_data.get('country', 'Unknown'))
    else:
        nicknames.append('Unknown')
        countries.append('Unknown')


# Add the new columns to the DataFrame
teams_df['team_name'] = nicknames
teams_df['country'] = countries

# Add stats columns to teams_df using Statbotics API
start_stats = []
pre_champs_stats = []
max_stats = []

for _, row in teams_df.iterrows():
    team_number = row['team_nr']
    try:
        # Fetch stats for the team using Statbotics API
        team_stats = sb.get_team_year(team_number, 2025)
        epa_stats = team_stats.get('epa', {}).get('stats', {})
        start_stats.append(epa_stats.get('start', float('nan')))
        pre_champs_stats.append(epa_stats.get('pre_champs', float('nan')))
        max_stats.append(epa_stats.get('max', float('nan')))
    except Exception as e:
        # Handle cases where the API call fails
        start_stats.append(float('nan'))
        pre_champs_stats.append(float('nan'))
        max_stats.append(float('nan'))


# Add the new columns to the DataFrame
teams_df['start_stats'] = start_stats
teams_df['pre_champs_stats'] = pre_champs_stats
teams_df['max_stats'] = max_stats

# Add binary columns for event codes
teams_df['2026tuis'] = (teams_df['event_code'] == '2026tuis').astype(int)
teams_df['2026tuis4'] = (teams_df['event_code'] == '2026tuis4').astype(int)

# Drop the original event_code column
teams_df.drop(columns=['event_code'], inplace=True)

# Merge duplicate team_nr entries by summing only the binary columns
binary_columns = ['2026tuis', '2026tuis4']
teams_df = teams_df.groupby('team_nr', as_index=False).agg(
    {**{col: 'sum' for col in binary_columns}, **{col: 'first' for col in teams_df.columns if col not in binary_columns + ['team_nr']}}
)

# Prepare columns for EPA and OPR
epa_total_points = []
epa_auto_points = []
epa_teleop_points = []
epa_endgame_points = []
opr_first_event = []

list_of_team_numbers = teams_df['team_nr'].tolist()

for team_number in list_of_team_numbers:
    year = 2025  # Last year

    # Fetch events for the team
    events_url = f"{TBA_BASE_URL}/team/frc{team_number}/events/{year}"
    events_response = requests.get(events_url, headers=headers)

    if events_response.status_code == 200:
        events = events_response.json()
        if events:
            # Sort events by start date and get the first event
            first_event = sorted(events, key=lambda e: e.get('start_date', ''))[0]
            event_key = first_event['key']

            # Fetch OPR for the first event
            opr_url = f"{TBA_BASE_URL}/event/{event_key}/oprs"
            opr_response = requests.get(opr_url, headers=headers)

            if opr_response.status_code == 200:
                opr_data = opr_response.json()
                opr_first_event.append(round(opr_data.get('oprs', {}).get(f"frc{team_number}", float('nan')), 2))
            else:
                opr_first_event.append(float('nan'))

            # Fetch EPA after the first event using Statbotics
            try:
                epa_data = sb.get_team_event(team_number, event_key)
                epa_breakdown = epa_data.get('epa', {}).get('breakdown', {})
                epa_total_points.append(epa_breakdown.get('total_points', float('nan')))
                epa_auto_points.append(epa_breakdown.get('auto_points', float('nan')))
                epa_teleop_points.append(epa_breakdown.get('teleop_points', float('nan')))
                epa_endgame_points.append(epa_breakdown.get('endgame_points', float('nan')))
            except Exception:
                epa_total_points.append(float('nan'))
                epa_auto_points.append(float('nan'))
                epa_teleop_points.append(float('nan'))
                epa_endgame_points.append(float('nan'))
        else:
            # No events found for the team
            opr_first_event.append(float('nan'))
            epa_total_points.append(float('nan'))
            epa_auto_points.append(float('nan'))
            epa_teleop_points.append(float('nan'))
            epa_endgame_points.append(float('nan'))
    else:
        # Failed to fetch events
        opr_first_event.append(float('nan'))
        epa_total_points.append(float('nan'))
        epa_auto_points.append(float('nan'))
        epa_teleop_points.append(float('nan'))
        epa_endgame_points.append(float('nan'))
    
    print(f"team: {team_number}, event: {event_key}, opr: {opr_first_event[-1]}, epa_total: {epa_total_points[-1]}, epa_auto: {epa_auto_points[-1]}, epa_teleop: {epa_teleop_points[-1]}, epa_endgame: {epa_endgame_points[-1]}")

    
# Add the new columns to the DataFrame
teams_df['epa_total_points'] = epa_total_points
teams_df['epa_auto_points'] = epa_auto_points
teams_df['epa_teleop_points'] = epa_teleop_points
teams_df['epa_endgame_points'] = epa_endgame_points
teams_df['opr_first_event'] = opr_first_event

print("Data collection complete.")

# output teams_df to csv
teams_df.to_csv("teams_with_stats.csv", index=False)

print("Saved collected data to teams_with_stats.csv")