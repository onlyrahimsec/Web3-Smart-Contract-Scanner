import subprocess
import json
import os

def get_vulnerability_details(check_name):
    # Simple Keyword Matching
    details = {
        "reentrancy": {"impact": "🔴 HIGH: Funds drain risk.", "fix": "Use Checks-Effects-Interactions."},
        "suicidal": {"impact": "🔴 HIGH: Unprotected selfdestruct.", "fix": "Add access control."},
        "solc-version": {"impact": "🔵 INFO: Old version.", "fix": "Use ^0.8.0."}
    }
    for key, val in details.items():
        if key in check_name.lower(): return val
    return {"impact": "Security Risk", "fix": "Review logic manually."}

def run_slither_scan(file_path):
    # Transforming the Docker Flash
    abs_path = os.path.abspath(file_path).replace('\\', '/')
    file_dir = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    
    if abs_path[1] == ':':
        drive = abs_path[0].lower()
        file_dir_docker = f"/{drive}{file_dir[2:]}"
    else:
        file_dir_docker = file_dir

    cmd = f'docker run --rm -v "{file_dir}":/share trailofbits/eth-security-toolbox slither /share/{file_name} --json -'
    
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=100)
        
        if stdout and '{' in stdout:
            return json.loads(stdout)
        else:
            # if nothing is found then the error will show up on terminal
            print(f"--- Slither Debug Error ---\n{stderr}")
            return None
    except Exception as e:
        print(f"System Error: {e}")
        return None

def run_mythril_scan(file_path):
    abs_path = os.path.abspath(file_path).replace('\\', '/')
    file_dir = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    
    cmd = f'docker run --rm -v "{file_dir}":/share mythril/myth analyze /share/{file_name} -o json'
    
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=300)
        
        if stdout and ('[' in stdout or '{' in stdout):
            data = json.loads(stdout)
            return data if isinstance(data, list) else data.get('issues', [])
        else:
            print(f"--- Mythril Debug Error ---\n{stderr}")
            return None
    except Exception as e:
        print(f"System Error: {e}")
        return None
