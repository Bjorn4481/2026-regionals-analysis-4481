# Configuration file for event analysis

# Blue Alliance API credentials
TBA_API_KEY = "YOUR_API_KEY_HERE"
TBA_BASE_URL = "https://www.thebluealliance.com/api/v3"

# Event codes to analyze with their display names
# Update this dictionary to change which events you want to analyze
EVENTS = {
    "2026tuis": "Istanbul Regional",
    "2026tuis4": "Yeditepe Regional",
}

# Year prefix for event codes (e.g., 2026)
EVENT_YEAR = "2026"

# Reference year for historical data (last year with complete data)
REFERENCE_YEAR = 2025

# X% Rule Configuration
# Estimated maximum points the best robot in the world will score on average (100% reference)
MAX_POINTS_ESTIMATE = 120  # Adjust this based on your team's analysis

# Reference percentages to display on plots
REFERENCE_PERCENTAGES = [50, 60, 70]  # e.g., 50%, 60%, 70% of max

# Validation
def validate_config():
    """Validate configuration settings."""
    errors = []
    
    # Validate TBA API key
    if not TBA_API_KEY or TBA_API_KEY == "YOUR_API_KEY_HERE":
        errors.append("TBA_API_KEY is not set. Get one from https://www.thebluealliance.com/account")
    
    # Validate events match EVENT_YEAR
    for event_code in EVENTS.keys():
        if not event_code.startswith(EVENT_YEAR):
            errors.append(f"Event code '{event_code}' does not match EVENT_YEAR '{EVENT_YEAR}'")
    
    # Validate year values
    if not EVENT_YEAR.isdigit() or len(EVENT_YEAR) != 4:
        errors.append(f"EVENT_YEAR must be a 4-digit year, got: {EVENT_YEAR}")
    
    if not isinstance(REFERENCE_YEAR, int) or REFERENCE_YEAR < 2000 or REFERENCE_YEAR > 2100:
        errors.append(f"REFERENCE_YEAR must be a valid year between 2000-2100, got: {REFERENCE_YEAR}")
    
    # Validate EVENTS is not empty
    if not EVENTS:
        errors.append("EVENTS dictionary is empty. Add at least one event.")
    
    return errors
