# 2026 Regionals Analysis

This project collects and analyzes data for FRC teams participating in the 2026 regionals. It uses data from The Blue Alliance (TBA) and Statbotics APIs to generate insights and visualizations. Some event_keys are hardcoded for simplicity.

## Project Structure
- **`collect_data.py`**: Collects team data from TBA and Statbotics APIs and saves it to `teams_with_stats.csv`.
- **`generate_plots.py`**: Generates visualizations (bubble plots and bar charts) based on the collected data.
- **`list_of_teams.csv`**: Input file containing team numbers and event codes.
- **`teams_with_stats.csv`**: Output file with enriched team data.

## Usage
1. Set your TBA API key in `collect_data.py`.
2. Run `collect_data.py` to collect data:
   ```bash
   python collect_data.py
   ```
3. Run `generate_plots.py` to generate visualizations:
   ```bash
   python generate_plots.py
   ```

## Requirements
- Python 3.x
- Libraries: pandas, matplotlib, numpy, requests, statbotics

## Notes
- Ensure list_of_teams.csv is populated with the correct team numbers and event codes.
- Replace "YOUR_TBA_API_KEY_HERE" in collect_data.py with your TBA API key.