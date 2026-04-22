<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=30&pause=1000&color=00FF41&center=true&vCenter=true&width=700&lines=Web3+Smart+Contract+Scanner;Automated+Security+Auditing+Tool;Powered+by+Slither+%2B+Docker" alt="Typing SVG" />

<br/>

```
███████╗███╗   ███╗ █████╗ ██████╗ ████████╗     ██████╗ ██████╗ ███╗   ██╗████████╗
██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝
███████╗██╔████╔██║███████║██████╔╝   ██║       ██║     ██║   ██║██╔██╗ ██║   ██║   
╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║       ██║     ██║   ██║██║╚██╗██║   ██║   
███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║       ╚██████╗╚██████╔╝██║ ╚████║   ██║   
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝  
                   ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗      
                   ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗     
                   ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝     
                   ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗     
                   ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║     
                   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   
```

<br/>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Required-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Slither](https://img.shields.io/badge/Slither-Static%20Analysis-FF6B35?style=for-the-badge&logo=ethereum&logoColor=white)](https://github.com/crytic/slither)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.x-363636?style=for-the-badge&logo=solidity&logoColor=white)](https://soliditylang.org)
[![License](https://img.shields.io/badge/License-MIT-00C896?style=for-the-badge)](LICENSE)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen?style=for-the-badge)](https://github.com/onlyrahimsec/Web3-Smart-Contract-Scanner)

<br/>

> **⚡ High-performance automated security auditing for Ethereum smart contracts.**  
> Identify critical vulnerabilities before deployment — with just a few clicks.

<br/>

[🚀 Quick Start](#-quick-start) • [🎯 Features](#-features) • [🏗 Architecture](#-technical-architecture) • [📦 Installation](#-installation) • [🖥 Usage](#-usage) • [🛡 Vulnerabilities Detected](#-vulnerabilities-detected) • [👤 Author](#-author)

---

</div>

## 🎯 Features

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     SCANNER CAPABILITY MATRIX                           │
├──────────────────────────────────┬──────────────────────────────────────┤
│  ✅ Reentrancy Detection          │  ✅ Access Control Analysis           │
│  ✅ Integer Overflow/Underflow    │  ✅ Unchecked Return Values           │
│  ✅ Timestamp Dependency          │  ✅ Uninitialized Storage Pointers    │
│  ✅ Delegate Call Vulnerabilities │  ✅ Front-Running Susceptibility      │
│  ✅ Self-Destruct Risks           │  ✅ Gas Optimization Issues           │
│  ✅ Isolated Docker Execution     │  ✅ Intuitive GUI Interface           │
└──────────────────────────────────┴──────────────────────────────────────┘
```

- 🔍 **Deep Static Analysis** — Powered by [Slither](https://github.com/crytic/slither), the industry-standard Solidity analysis framework by Trail of Bits
- 🐳 **Docker Isolated** — Every scan runs in a sandboxed container; no environment pollution, no version conflicts
- 🖥️ **Modern GUI** — Built with `customtkinter` for a clean, distraction-free auditing experience
- ⚡ **Fast Results** — Seconds-to-audit pipeline from paste-to-report
- 🔄 **Multi-Compiler Support** — Handles multiple `solc` versions seamlessly inside the container
- 📋 **Structured Reports** — Findings categorized by severity: High / Medium / Low / Informational

---

## 🏗 Technical Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│    ┌──────────────┐        ┌──────────────────────────────────────┐   │
│    │   User GUI   │        │         Docker Container             │   │
│    │  (gui.py)    │        │   trailofbits/eth-security-toolbox   │   │
│    │              │        │                                      │   │
│    │  customtkinter│──────▶│  ┌─────────┐    ┌────────────────┐  │   │
│    │              │ stdin  │  │ Slither │───▶│ Vulnerability  │  │   │
│    │  Contract    │        │  │ Engine  │    │   Detectors    │  │   │
│    │  Input Field │        │  └─────────┘    └───────┬────────┘  │   │
│    │              │◀───────│                          │           │   │
│    │  Results     │ stdout │  ┌───────────────────────▼────────┐  │   │
│    │  Viewer      │        │  │     JSON / Text Report         │  │   │
│    └──────────────┘        │  └────────────────────────────────┘  │   │
│                            └──────────────────────────────────────┘   │
│                                                                        │
│           Python Orchestration Layer (Subprocess + Docker API)         │
└────────────────────────────────────────────────────────────────────────┘
```

The scanner is a **Python-based orchestration layer** that:
1. Accepts Solidity source code via the GUI
2. Mounts the code into an isolated `trailofbits/eth-security-toolbox` Docker container
3. Executes Slither's full detector suite against the target contract
4. Parses and renders structured results back inside the GUI

---

## 📦 Installation

### Prerequisites

Before you begin, ensure the following are installed on your system:

| Tool | Version | Check Command |
|------|---------|---------------|
| Python | 3.8+ | `python --version` |
| Docker | 20.10+ | `docker --version` |
| Git | Any | `git --version` |

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/onlyrahimsec/Web3-Smart-Contract-Scanner.git
cd Web3-Smart-Contract-Scanner
```

### Step 2 — Install Python Dependencies

```bash
pip install --upgrade customtkinter
```

### Step 3 — Pull the Security Toolbox Image

```bash
docker pull trailofbits/eth-security-toolbox
```

> 💡 This image (~2GB) bundles Slither, Echidna, Manticore, and all required Solidity compilers. Pull once, audit forever.

### Step 4 — Launch the Scanner

```bash
python gui.py
```

---

## 🚀 Quick Start

```bash
# Clone → Install → Pull → Scan. That's it.
git clone https://github.com/onlyrahimsec/Web3-Smart-Contract-Scanner.git
cd Web3-Smart-Contract-Scanner
pip install --upgrade customtkinter
docker pull trailofbits/eth-security-toolbox
python gui.py
```

---

## 🖥 Usage

Once the GUI launches:

```
 ┌─────────────────────────────────────────────────────┐
 │        Web3 Smart Contract Scanner v1.0             │
 │─────────────────────────────────────────────────────│
 │                                                     │
 │  📂  Load Contract File  [  Browse...  ]            │
 │                                                     │
 │  ─────────────────────────────────────────────────  │
 │  |  pragma solidity ^0.8.0;                       | │
 │  |  contract Vulnerable {                         | │
 │  |      mapping(address => uint) public bal;      | │
 │  |      ...                                       | │
 │  ─────────────────────────────────────────────────  │
 │                                                     │
 │              [ 🔍  Run Audit ]                      │
 │                                                     │
 │  ── RESULTS ──────────────────────────────────────  │
 │  [HIGH]   Reentrancy in withdraw() — Line 42       │
 │  [MEDIUM] Unchecked return value — Line 78         │
 │  [LOW]    Timestamp dependency — Line 95           │
 └─────────────────────────────────────────────────────┘
```

1. **Load** your `.sol` file using the file browser, or paste code directly
2. Click **Run Audit** — the Docker engine spins up automatically
3. Review findings categorized by severity in the results panel
4. Fix vulnerabilities and re-scan until clean ✅

---

## 🛡 Vulnerabilities Detected

| Severity | Vulnerability Type | Impact |
|----------|--------------------|--------|
| 🔴 **HIGH** | Reentrancy | Fund drainage |
| 🔴 **HIGH** | Unprotected `selfdestruct` | Contract destruction |
| 🔴 **HIGH** | Arbitrary `delegatecall` | Full takeover |
| 🟠 **MEDIUM** | Integer overflow/underflow | Logic bypass |
| 🟠 **MEDIUM** | Access control issues | Unauthorized calls |
| 🟠 **MEDIUM** | Unchecked return values | Silent failures |
| 🟡 **LOW** | Timestamp dependency | Minor manipulation |
| 🟡 **LOW** | Uninitialized storage | Unpredictable state |
| 🔵 **INFO** | Gas inefficiency | Optimization hints |
| 🔵 **INFO** | Code style warnings | Best practice notes |

---

## 📁 Project Structure

```
Web3-Smart-Contract-Scanner/
│
├── 📄 gui.py                  # Main GUI orchestration script
├── 📄 requirements.txt        # Python dependencies
├── 📄 README.md               # You are here
├── 📄 LICENSE                 # MIT License
│
├── 📂 contracts/              # Sample vulnerable contracts for testing
│   ├── reentrancy_demo.sol
│   └── overflow_demo.sol
│
└── 📂 reports/                # Exported audit reports (generated at runtime)
```

---

## ⚙️ Configuration

| Option | Default | Description |
|--------|---------|-------------|
| Docker Image | `trailofbits/eth-security-toolbox` | Security analysis container |
| Analyzer | `Slither` | Static analysis engine |
| Output Format | Plain Text + JSON | Report format |
| Timeout | 120s | Max scan duration per contract |

---

## 🤝 Contributing

Contributions are welcome and encouraged!

```
Fork → Branch → Commit → Pull Request
```

1. **Fork** the repository
2. Create your feature branch: `git checkout -b feature/better-detector`
3. Commit your changes: `git commit -m "feat: add new detector for X"`
4. Push to the branch: `git push origin feature/better-detector`
5. Open a **Pull Request**

Please open an **Issue** first for major changes so we can discuss the approach.

---

## ⚠️ Disclaimer

> This tool is intended **exclusively for educational and ethical security research purposes**.  
> Only scan contracts you own or have explicit permission to audit.  
> The author assumes no liability for misuse of this tool.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

---

<div align="center">

## 👤 Author

**Md Rahim Rahman**

[![GitHub](https://img.shields.io/badge/GitHub-onlyrahimsec-181717?style=for-the-badge&logo=github)](https://github.com/onlyrahimsec)

<br/>

*Built with ❤️ for the Web3 security community*

<br/>

---

⭐ **If this tool helped you secure a contract, please consider giving it a star!** ⭐

```

 |_____/   |_|  |_| |_|_|  \_\ |_____/|_| |_|_|  |_|_____(_)
```

</div>
