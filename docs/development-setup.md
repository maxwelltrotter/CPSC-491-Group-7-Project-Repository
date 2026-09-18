# AI-IDS Development Environment Setup

## Prerequisites

- **Git**
- **Python 3.11**
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
py -3.11 -m venv .venv
.venv\Scripts\activate
```

for macOS/Linux:
```
python3.11 -m venv .venv
source .venv/bin/activate
```

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
python scripts/verify_environment.py
pytest
```

