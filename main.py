"""
Main script to run the complete analysis pipeline:
1. Generate team list from event codes
2. Collect team data from TBA and Statbotics APIs
3. Generate plots
"""

import subprocess
import sys

def run_script(script_name, description):
    """Run a Python script and handle errors."""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True,
    )
    
    # Print any standard output from the script so users still see progress
    if result.stdout:
        print(result.stdout, end="")
    
    if result.returncode != 0:
        print(f"\n❌ Error running {script_name}")
        # Include captured output to aid debugging
        if result.stderr:
            print("\n--- Error Output ---")
            print(result.stderr, end="")
        sys.exit(1)
    
    print(f"\n✅ Completed: {description}")

def main():
    print("Starting complete analysis pipeline...")
    print(f"Python executable: {sys.executable}")
    
    # Step 1: Generate team list
    run_script("generate_team_list.py", "Generate team list from event codes")
    
    # Step 2: Collect data
    run_script("collect_data.py", "Collect team data from APIs")
    
    # Step 3: Generate plots
    run_script("generate_plots.py", "Generate analysis plots")
    
    print("\n" + "="*60)
    print("🎉 COMPLETE! All steps finished successfully.")
    print("="*60)

if __name__ == "__main__":
    main()
