# 2026 Regionals Analysis

This project collects and analyzes data for FRC teams participating in the 2026 events. It uses data from The Blue Alliance (TBA) and Statbotics APIs to generate insights and visualizations based on the X% Rule methodology from Team Rembrandts.

## Project Structure
- **`config.py`**: Centralized configuration file for API keys, event codes, and X% Rule parameters
- **`main.py`**: Main script that runs the complete analysis pipeline
- **`generate_team_list.py`**: Fetches team lists from TBA API based on configured event codes
- **`collect_data.py`**: Collects team data from TBA and Statbotics APIs and saves it to `teams_with_stats.csv`
- **`generate_plots.py`**: Generates visualizations (bubble plots and bar charts) with performance reference lines
- **`requirements.txt`**: Python dependencies for the project
- **`list_of_teams.csv`**: Generated file containing team numbers and event codes
- **`teams_with_stats.csv`**: Generated file with enriched team data

## Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configure
Edit `config.py` to set:
- **`TBA_API_KEY`**: Your Blue Alliance API key
- **`EVENTS`**: Dictionary of event codes and display names
- **`EVENT_YEAR`**: Year prefix for event codes (e.g., "2026")
- **`REFERENCE_YEAR`**: Year to use for historical team data (e.g., 2025)
- **`MAX_POINTS_ESTIMATE`**: Estimated average max points for the best robot (100% reference)
- **`REFERENCE_PERCENTAGES`**: Performance target percentages to display on plots

### 3. Run Analysis
```bash
# Run complete pipeline (recommended)
python main.py

# Or run steps individually:
python generate_team_list.py  # Step 1: Fetch team lists
python collect_data.py         # Step 2: Collect team data
python generate_plots.py       # Step 3: Generate visualizations
```

## Configuration

All configuration is centralized in `config.py`:

```python
# Event codes to analyze
EVENTS = {
    "2026tuis": "Istanbul Regional",
    "2026tuis4": "Yeditepe Regional",
}

# Year prefix for event codes
EVENT_YEAR = "2026"

# Reference year for historical data
REFERENCE_YEAR = 2025

# X% Rule Configuration
MAX_POINTS_ESTIMATE = 120  # 100% reference point
REFERENCE_PERCENTAGES = [50, 60, 70]  # Target percentages
```

## X% Rule Methodology

This project implements the X% Rule from Team Rembrandts:
- **100% reference**: Estimated max points the best robot in the world will score on average
- **Target percentage**: Design goal (e.g., 70% = 84 points if max is 120)
- Plots show reference lines for configured percentages to evaluate team performance

## Requirements
- Python 3.x
- Libraries: pandas, matplotlib, numpy, requests, statbotics (see `requirements.txt`)

## Output
- `list_of_teams.csv`: Team numbers and event codes
- `teams_with_stats.csv`: Enriched team data (EPA, OPR, team info)
- `bubble_*.png`: Auto vs Teleop EPA scatter plots with Endgame EPA as bubble size
- `bar_top*_*.png`: Top teams comparison charts with reference lines