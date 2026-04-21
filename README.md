# Web3 Smart Contract Vulnerability Scanner

A high-performance automated security auditing tool designed for Ethereum smart contracts. This application leverages the Slither static analysis framework within isolated Docker containers to identify critical security flaws in Solidity source code. Developed with a focus on usability and precision, it provides security researchers and developers with an intuitive interface to conduct deep-dive audits of smart contracts before deployment.

---

## Technical Architecture
The scanner operates as a Python-based orchestration layer that communicates with specialized security engines. By utilizing Docker, the tool ensures a consistent execution environment, eliminating versioning conflicts between different Solidity compilers and the analysis tools.

---

## Key Security Detectors
The scanner is configured to detect over 100 vulnerability patterns, with a primary focus on:

* **Re-entrancy Vulnerabilities:** Identifying unsafe external calls that allow state manipulation.
* **Integer Overflow and Underflow:** Highlighting arithmetic operations that could lead to unexpected behavior.
* **Access Control Flaws:** Detecting unprotected administrative functions and ownership issues.
* **Low-Level Calls:** Flagging the use of call, delegatecall, and send which may bypass safety checks.
* **Uninitialized State Variables:** Identifying variables that could lead to contract failure or exploitation.

---

## System Requirements
The scanner requires a specific environment to ensure high-fidelity analysis and containerized execution of security engines.

| Component | Minimum Requirement | Purpose |
| :--- | :--- | :--- |
| **Python** | 3.10 or Higher | Core Application Logic |
| **Docker Engine** | 20.10.x + | Isolated Analysis Environment |
| **OS** | Windows 10/11 (WSL2), Linux, macOS | Cross-platform Compatibility |
| **Memory** | 4GB RAM | Handling Large Contract ASTs |

### External Resources
* **Python Runtime:** [Download Official Binaries](https://www.python.org/downloads/)
* **Docker Engine:** [Get Docker Desktop](https://www.docker.com/products/docker-desktop/)
* **Security Engine:** Powered by [Trail of Bits Slither](https://github.com/crytic/slither)

---

## Deployment and Installation

Follow these steps to deploy the scanner in your local security research environment.

### 1. Repository Acquisition
Initialize git and clone the project directory to your local workstation:
```bash
git clone [https://github.com/onlyrahimsec/Web3-Smart-Contract-Scanner.git](https://github.com/onlyrahimsec/Web3-Smart-Contract-Scanner.git)
cd Web3-Smart-Contract-Scanner


### 2. Dependency Resolution
Install the necessary graphical interface libraries and verify the environment:
```bash
pip install --upgrade customtkinter
