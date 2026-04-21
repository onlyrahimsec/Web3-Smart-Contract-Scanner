import subprocess
import os

def run_slither_scan(contract_path):
    print(f"--- [!] {contract_path} ফাইলটি স্ক্যান করা হচ্ছে ---")
    
    # ডকার ব্যবহার করে Slither চালানোর কমান্ড
    # এটি আপনার ফাইলটিকে ডকারের ভেতরে নিয়ে স্ক্যান করবে
    cmd = f"docker run -v {os.getcwd()}:/share trailofbits/eth-security-toolbox slither /share/{contract_path}"
    
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

if __name__ == "__main__":
    file_name = "test.sol" # আমরা একটু পরেই এই ফাইলটি বানাবো
    report = run_slither_scan(file_name)
    print(report)