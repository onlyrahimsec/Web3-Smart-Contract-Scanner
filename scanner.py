import subprocess
import json
import os

VULN_DB = {
    "reentrancy-eth": {
        "impact": "🔴 HIGH",
        "desc": "External calls can be hijacked to drain funds before state update.",
        "fix": "Use the Checks-Effects-Interactions pattern or ReentrancyGuard."
    },
    "suicidal": {
        "impact": "🔴 HIGH",
        "desc": "Anyone can trigger selfdestruct to destroy the contract.",
        "fix": "Remove selfdestruct or restrict access using onlyOwner modifiers."
    },
    "unchecked-send": {
        "impact": "🟠 MEDIUM",
        "desc": "The return value of an external call is not checked, leading to silent failures.",
        "fix": "Use require() to verify the success of call/send operations."
    },
    "solc-version": {
        "impact": "🔵 INFO",
        "desc": "Outdated compiler version detected. Newer versions have built-in security features.",
        "fix": "Upgrade to a stable version like ^0.8.0."
    }
}

def get_vulnerability_details(check_name):
    for key in VULN_DB:
        if key in check_name.lower():
            return VULN_DB[key]
    return {
        "impact": "Potential Risk",
        "desc": "A potential security issue was detected during static/symbolic analysis.",
        "fix": "Perform a manual code review and follow SWC registry guidelines."
    }

def run_slither_scan(file_path):
    abs_path = os.path.abspath(file_path).replace('\\', '/')
    file_dir = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    cmd = f'docker run --rm -v "{file_dir}:/share" trailofbits/eth-security-toolbox slither /share/{file_name} --json -'
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = process.communicate(timeout=120)
        return json.loads(stdout) if stdout else None
    except: return None

def run_mythril_scan(file_path):
    abs_path = os.path.abspath(file_path).replace('\\', '/')
    file_dir = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    cmd = f'docker run --rm -v "{file_dir}:/share" mythril/myth analyze /share/{file_name} -o json'
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = process.communicate(timeout=300)
        if stdout:
            data = json.loads(stdout)
            return data if isinstance(data, list) else data.get('issues', [])
        return None
    except: return None
