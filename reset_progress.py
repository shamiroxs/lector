import json
import os

progress_file = "progress.json"

def reset_progress():
    """Save the last completed chapter to the progress file."""
    progress = {"last_completed_chapter": 0}
    with open(progress_file, 'w') as file:
        json.dump(progress, file)
    print(f"Progress reset to 0")
    
    
if __name__ == "__main__":
    reset_progress()

