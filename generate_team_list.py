print("Generating team list from event codes...")

import requests
import pandas as pd
import sys
from config import TBA_API_KEY, TBA_BASE_URL, EVENTS, REQUEST_TIMEOUT, validate_config

# Validate configuration
config_errors = validate_config()
if config_errors:
    print("[ERROR] Configuration errors:")
    for error in config_errors:
        print(f"  - {error}")
    sys.exit(1)

# Event codes are configured in config.py
event_codes = list(EVENTS.keys())

# Prepare lists for the DataFrame
team_numbers = []
event_codes_list = []

# Track event processing
successful_events = []
failed_events = []

headers = {"X-TBA-Auth-Key": TBA_API_KEY}

# Fetch teams for each event
for event_code in event_codes:
    print(f"Fetching teams for event: {event_code}")
    
    try:
        # Get teams for this event
        response = requests.get(f"{TBA_BASE_URL}/event/{event_code}/teams/simple", headers=headers, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 401:
            print(f"[ERROR] Invalid TBA API key. Please check your API key in config.py")
            sys.exit(1)
        elif response.status_code == 404:
            print(f"[WARNING] Event '{event_code}' not found. It may not exist yet or the code is incorrect.")
            failed_events.append((event_code, "Not found (404)"))
            continue
        elif response.status_code == 429:
            print(f"[ERROR] Rate limit exceeded. Please wait a few minutes and try again.")
            sys.exit(1)
        elif response.status_code == 200:
            teams = response.json()
            
            if not teams:
                print(f"[WARNING] No teams found for event '{event_code}'")
                failed_events.append((event_code, "No teams"))
                continue
                
            print(f"Found {len(teams)} teams for {event_code}")
            successful_events.append((event_code, len(teams)))
            
            for team in teams:
                team_number = team['team_number']
                team_numbers.append(team_number)
                event_codes_list.append(event_code)
        else:
            print(f"[WARNING] Unexpected status code {response.status_code} for event {event_code}")
            failed_events.append((event_code, f"Status {response.status_code}"))
            continue
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timeout for event {event_code}. Check your internet connection.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Connection failed. Please check your internet connection.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Error fetching teams for {event_code}: {str(e)}")
        sys.exit(1)

# Create DataFrame
teams_df = pd.DataFrame({
    'team_nr': team_numbers,
    'event_code': event_codes_list
})

if teams_df.empty:
    print("[ERROR] No teams were found for any event. Cannot create team list.")
    sys.exit(1)

# Sort by event_code and then by team_nr (numerically)
teams_df = teams_df.sort_values(['event_code', 'team_nr'])

# Save to CSV
output_file = "list_of_teams.csv"
try:
    teams_df.to_csv(output_file, index=False)
    print(f"\n[SUCCESS] Saved {len(teams_df)} team entries to {output_file}")
    print(f"Unique teams: {teams_df['team_nr'].nunique()}")
    
    # Print summary
    if successful_events:
        print(f"\n[INFO] Successfully fetched {len(successful_events)} event(s):")
        for event_code, team_count in successful_events:
            print(f"  * {event_code}: {team_count} teams")
    
    if failed_events:
        print(f"\n[WARNING] Failed to fetch {len(failed_events)} event(s):")
        for event_code, reason in failed_events:
            print(f"  * {event_code}: {reason}")
except Exception as e:
    print(f"[ERROR] Error saving to {output_file}: {str(e)}")
    sys.exit(1)
