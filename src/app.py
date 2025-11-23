import os
import sys
import subprocess

def main():
    #ENTRY POINT
    print("Starting TSP Visualization App...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    streamlit_app_path = os.path.join(current_dir, "web", "app.py")
    
    cmd = [sys.executable, "-m", "streamlit", "run", streamlit_app_path]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nApp stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"Error running app: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()