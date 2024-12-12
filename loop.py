import subprocess

def run_script(script_name):
    try:
        print(f"Executing {script_name}...")
        # Run the script using subprocess
        result = subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing {script_name}: {e.stderr}")

if __name__ == "__main__":
    # Define the scripts to run in order
    scripts = ['text.py', 'audio.py', 'video.py']
    
    # Execute each script in order
    for script in scripts:
        run_script(script)

    print("All scripts executed successfully.")
