import os
import platform
import subprocess
import sys

def create_virtualenv():
    # Check OS type
    os_type = platform.system().lower()

    # Create venv folder path
    venv_folder = os.path.join(os.getcwd(), "venv")
    
    if not os.path.exists(venv_folder):
        if os_type == "windows":
            print("Detected Windows OS. Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"])
        elif os_type == "linux":
            print("Detected Linux (Ubuntu). Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"])
        else:
            print(f"Unsupported OS: {os_type}")
            sys.exit(1)
    else:
        print("Virtual environment already exists.")

def install_requirements():
    os_type = platform.system().lower()

    # Use the correct pip path based on OS
    if os_type == "windows":
        pip_executable = os.path.join("venv", "Scripts", "pip")
    else:  # Linux (Ubuntu)
        pip_executable = os.path.join("venv", "bin", "pip")

    # Check if requirements.txt exists
    if os.path.exists("requirements.txt"):
        print("Installing dependencies from requirements.txt...")
        subprocess.run([pip_executable, "install", "-r", "requirements.txt"])
    else:
        print("requirements.txt not found.")
        sys.exit(1)

def run_code():
    os_type = platform.system().lower()

    # Use the correct Python executable path based on OS
    if os_type == "windows":
        python_executable = os.path.join("venv", "Scripts", "python")
    else:  # Linux (Ubuntu)
        python_executable = os.path.join("venv", "bin", "python")

    print("Running the application...")
    subprocess.run([python_executable, "src/main.py"])

if __name__ == "__main__":
    create_virtualenv()       # Step 1: Create virtual environment
    install_requirements()    # Step 2: Install required dependencies
    run_code()                # Step 3: Run the application
