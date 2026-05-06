# 🛡️ CVE-2026-0300: PAN-OS User-ID™ Portal RCE Analysis
### **Research Proof-of-Concept: CWE-787 Out-of-bounds Write**

![Security](https://img.shields.io/badge/Security-Critical-red) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)

## 📌 Overview
**CVE-2026-0300** is a high-severity buffer overflow vulnerability identified in the **Palo Alto Networks PAN-OS** User-ID™ Authentication Portal (Captive Portal). This research repository demonstrates the technical logic of the vulnerability, specifically focusing on how an unauthenticated network packet can lead to **Remote Code Execution (RCE)** with root privileges.

---

## 📊 Vulnerability Breakdown
| Feature | Details |
| :--- | :--- |
| **CVE ID** | CVE-2026-0300 |
| **Severity Score** | 9.3 (Critical) |
| **Weakness Type** | CWE-787: Out-of-bounds Write |
| **Attack Vector** | Network (Unauthenticated) |
| **Privileges Required** | None |
| **User Interaction** | None |
| **Affected Software** | PAN-OS 12.1, 11.2, 11.1, 10.2 |

---

## 🔬 Technical Mechanism
The vulnerability occurs when the User-ID Authentication Portal service fails to validate the length of incoming data before writing it to a memory buffer. 

1. **The Buffer:** The service allocates a fixed-size memory area for processing portal requests.
2. **The Overflow:** A specially crafted POST request sends a payload exceeding this size.
3. **The Overwrite:** Excess data overwrites the stack/heap, allowing the attacker to control the **Instruction Pointer (EIP/RIP)** and execute arbitrary shellcode.

---

## 🛠️ Installation & Setup

### **1. Prerequisites**
* Python 3.9 or higher.
* **No external libraries required** (Uses standard `socket`, `struct`, and `argparse`).

### **2. Cloning the Research Tool**
# Clone the repository

```bash
git clone https://github.com/qassam-315/PAN-OS-CVE-2026-0300-Research.git
```

# Navigate to the folder

```bash
cd PAN-OS-CVE-2026-0300-Research
```

# Make the script executable

```bash
chmod +x research_poc.py
```
## 🚀 Usage Guide
This tool is designed with a professional CLI (Command Line Interface).
### **Basic Command**

```bash
python3 research_poc.py -t <TARGET_IP>
```
### **Advanced Parameters**
| Flag | Name | Description | Default |
|---|---|---|---|
| -t | --target | **(Required)** Target IP address of the firewall. | N/A |
| -p | --port | The port running the User-ID Portal. | 6082 |
| -o | --offset | The byte length to reach the memory overflow point. | 2048 |
| -r | --ret | The Hexadecimal return address. | 0xdeadbeef |
## 🛡️ Mitigation & Safety
 * **Update PAN-OS:** Install the latest security patches (Released May 2026).
 * **IP Restriction:** Restrict portal access to trusted internal IP zones.
 * **Disable Portal:** If User-ID Authentication is not required, disable the feature.
## ⚠️ Ethical & Legal Disclaimer
**FOR EDUCATIONAL AND AUTHORIZED RESEARCH ONLY.** Unauthorized testing against systems you do not own is illegal. The author is not responsible for any misuse of this research code. Use responsibly to improve global security.
**Developed By:** qassam-315
**Vulnerability Discovery Date:** May 06, 2026

