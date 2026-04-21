# Web3 Smart Contract Vulnerability Scanner

A high-performance automated security auditing tool designed for Ethereum smart contracts. This application leverages the Slither static analysis framework within isolated Docker containers to identify critical security flaws in Solidity source code.

---

## Technical Architecture
The scanner operates as a Python-based orchestration layer that communicates with specialized security engines. By utilizing Docker, the tool ensures a consistent execution environment.

---

## Deployment and Installation

### 1. Repository Acquisition
Initialize git and clone the project directory:
```bash
git clone [https://github.com/onlyrahimsec/Web3-Smart-Contract-Scanner.git](https://github.com/onlyrahimsec/Web3-Smart-Contract-Scanner.git)
cd Web3-Smart-Contract-Scanner

pip install --upgrade customtkinter

docker pull trailofbits/eth-security-toolbox

python gui.py
