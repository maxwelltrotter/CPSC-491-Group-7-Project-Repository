# AI-IDS Development Environment Setup

## Prerequisites

- **Git**
- **Python 3.12**
- **Npcap** [version]
- A terminal or IDE
- Operating-system permissions required for future packet capture

## Clone the Repository

```bash
git clone https://github.com/maxwelltrotter/CPSC-491-Group-7-Project-Repository.git
cd CPSC-491-Group-7-Project-Repository
```

## 1. Create Virtual Environment
for Windows:
```
py -3.12 -m venv .venv
.venv\Scripts\activate
```

for macOS/Linux:
```
python3.12 -m venv .venv
source .venv/bin/activate
```

## 2. Install Windows System Dependencies
### Npcap
Installation required for packet capture in Scapy.

**Purpose:**
- Provides the Windows packet-capture driver.
- Allows Scapy to access network interfaces.
- Supports the packet-capture proof of concept for S1-09.

**Verification**

Run the following commands in PowerShell:

```powershell
Get-Service npcap -ErrorAction SilentlyContinue
```

```powershell
python -c "from scapy.all import get_if_list; print(get_if_list())"
```

```powershell
python -c "from scapy.all import sniff; sniff(count=5, store=False); print('Capture complete')"
```


**Installation:**

1. Open PowerShell.
2. Check whether WinGet is available:

   ```powershell
   winget --version
   ```

3. Search for Npcap:

   ```powershell
   winget search Npcap
   ```

4. If a verified package is available, install it using its exact
   package identifier. Otherwise, download the installer from:

   https://npcap.com/

5. Complete the installation using the required default settings.


## 2. Install Dependencies

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 3. Configure Environment Variables

Copy .env.example to .env.
Update local settings if necessary.

## 4. Verify the Environment
```
scripts/verify_environment.py
pytest
```

