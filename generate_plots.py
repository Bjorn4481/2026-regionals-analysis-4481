import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from config import EVENTS, MAX_POINTS_ESTIMATE, REFERENCE_PERCENTAGES, EVENT_YEAR, validate_config

# Validate configuration
config_errors = validate_config()
if config_errors:
    print("[ERROR] Configuration errors:")
    for error in config_errors:
        print(f"  - {error}")
    sys.exit(1)

# === CONFIGURATION ===
DATA_PATH = "teams_with_stats.csv"   # path to your dataset
TOP_N = 16                           # number of top teams per event
BUBBLE_SIZE_SCALE = 10               # bubble size multiplier
OUTPUT_DIR = "."                     # folder for saving images

# Calculate reference lines based on max points estimate
REFERENCE_LINES = {f"{pct}%": MAX_POINTS_ESTIMATE * pct / 100 for pct in REFERENCE_PERCENTAGES}

# === LOAD AND PREPARE DATA ===
if not os.path.exists(DATA_PATH):
    print(f"[ERROR] {DATA_PATH} not found. Run collect_data.py first.")
    sys.exit(1)

try:
    df = pd.read_csv(DATA_PATH)
    if df.empty:
        print(f"[ERROR] {DATA_PATH} is empty.")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Error reading {DATA_PATH}: {str(e)}")
    sys.exit(1)

df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Identify event columns (e.g. 2026tuis, 2026tuis4)
event_cols = [c for c in df.columns if EVENT_YEAR in c]
# Use event names from config
event_map = {c: EVENTS.get(c, c) for c in event_cols}

# Convert relevant columns to numeric
for col in ["epa_auto_points", "epa_teleop_points", "epa_endgame_points", "epa_total_points", "opr_first_event"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Create first_event_epa for convenience
df["first_event_epa"] = df["epa_total_points"]

# Identify team number and name columns
team_id_col = next((c for c in df.columns if any(k in c for k in ["team_number","team_nr","team","number","frc"])), None)
team_name_col = next((c for c in df.columns if any(k in c for k in ["team_name","name","nickname"])), None)

# Fallbacks if columns are missing
df["team_id"] = df[team_id_col] if team_id_col else np.arange(len(df))
df["team_name"] = df[team_name_col] if team_name_col else ""

# Convert event flags (1 = attending, 0 = not attending)
for c in event_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

# === PLOT PER EVENT ===
for event_col, event_name in event_map.items():
    if event_col not in df.columns:
        continue

    sub = df[df[event_col] == 1].copy()
    if sub.empty:
        print(f"[WARNING] No data for {event_name}")
        continue

    # Sort and get top N teams
    sub = sub.sort_values("first_event_epa", ascending=False)
    top = sub.head(TOP_N).copy()

    # --- Bubble Plot: Auto vs Teleop ---
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        sub["epa_teleop_points"],
        sub["epa_auto_points"],
        s=sub["epa_endgame_points"] * BUBBLE_SIZE_SCALE + 20,
        c=sub["first_event_epa"],
        cmap="plasma",
        alpha=0.7,
        edgecolors="black"
    )

    # Label top teams (by number)
    for _, row in top.iterrows():
        plt.text(
            row["epa_teleop_points"],
            row["epa_auto_points"] + 0.5,  # Offset text slightly above the bubble
            str(int(row["team_id"])),
            fontsize=8, ha="center", va="center",
            fontweight="bold", color="black"
        )

    plt.colorbar(scatter, label="First Event EPA")
    plt.title(f"{event_name}: Auto vs Teleop EPA (bubble = Endgame EPA)")
    plt.xlabel("Teleop EPA")
    plt.ylabel("Auto EPA")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/bubble_{event_col}.png", dpi=160)
    plt.close()

    # --- Grouped Bar Chart: EPA vs OPR ---
    x = np.arange(len(top))
    width = 0.35
    plt.figure(figsize=(10,5))
    plt.bar(x - width/2, top["first_event_epa"], width, label="First Event EPA")
    plt.bar(x + width/2, top["opr_first_event"], width, label="First Event OPR")

    # Reference lines
    for label, value in REFERENCE_LINES.items():
        plt.axhline(y=value, color="gray", linestyle="--", linewidth=1)
        plt.text(len(x) - 0.4, value + 1, label, color="gray", fontsize=8, va="bottom")

    plt.xticks(x, [int(t) for t in top["team_id"]], rotation=45)
    plt.xlabel("Team Number")
    plt.ylabel("Performance Metric")
    plt.title(f"Top {TOP_N} Teams — {event_name}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/bar_top{TOP_N}_{event_col}.png", dpi=160)
    plt.close()

print("[SUCCESS] Plots generated for all events!")
