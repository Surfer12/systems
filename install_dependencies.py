#!/usr/bin/env python3

def install_required_packages():
    import subprocess
    import sys
    
    required_packages = [
        "transformers",
        "torch",
        "numpy"
    ]
    
    for package in required_packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("All required packages installed successfully.")

if __name__ == "__main__":
    install_required_packages()
