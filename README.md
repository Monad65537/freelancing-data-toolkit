# DataClean Pro

**Automated CSV and Excel data cleaning, validation, and quality reporting**

## Overview

DataClean Pro is a Python-based command-line tool designed to clean and validate structured customer datasets.

It separates acceptable records from records requiring manual review and generates an audit report summarizing data-quality problems.

## Features

- Supports CSV and Excel (`.xlsx`) inputs.
- Preserves customer IDs with leading zeros when supplied as text.
- Standardizes column names and removes surrounding whitespace.
- Normalizes customer names and email capitalization.
- Identifies duplicate customer IDs.
- Flags malformed or negative amounts.
- Detects invalid dates and email formats.
- Preserves rejected records with explanatory rejection reasons.
- Generates CSV outputs, a JSON quality report, and an execution log.

## Installation

Requirements: Python 3.12 or a compatible version.

Clone the repository and navigate to its directory:

git clone https://github.com/Monad65537/freelancing-data-toolkit.git
cd freelancing-data-toolkit

Create a virtual environment:

py -3.12 -m venv .venv

Install the required dependencies:

.\.venv\Scripts\python.exe -m pip install pandas openpyxl pytest

Verify the installation:

.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe dataclean_cli.py --help

The help command should display the application's available arguments, including --input and --output.

Note: DataClean Pro currently runs directly from its source repository; this procedure installs the dependencies rather than a separately packaged application.

## Usage

Run the application from the repository root:

```bash
python dataclean_cli.py --input data/messy_customers.csv --output outputs
```

The program produces:

| File | Description |
|---|---|
| `cleaned_customers.csv` | Accepted records |
| `flagged_rows.csv` | Records requiring manual review |
| `quality_report.json` | Summary of data-quality problems |
| `execution.log` | Processing log |

### Inspecting the results

After running the application, open the specified output directory.

- **`cleaned_customers.csv`** contains accepted records that passed the implemented validation rules.
- **`flagged_rows.csv`** contains records requiring manual review, together with their rejection reasons.
- **`quality_report.json`** summarizes the processing results and data-quality findings.
- **`execution.log`** records execution messages, including the number of loaded, accepted, and flagged records.

To inspect the quality report in PowerShell:

```powershell
Get-Content outputs\quality_report.json
```

To inspect the first five accepted records:

```powershell
.\.venv\Scripts\python.exe -c "import pandas as pd; print(pd.read_csv('outputs/cleaned_customers.csv', dtype={'customer_id':'string'}).head())"
```

To inspect the first five flagged records:

```powershell
.\.venv\Scripts\python.exe -c "import pandas as pd; print(pd.read_csv('outputs/flagged_rows.csv', dtype={'customer_id':'string'}).head())"
```

Customer identifiers are explicitly loaded as strings to preserve leading zeros.

**Important:** Flagged records should be reviewed against the client's agreed validation rules before making any corrections or discarding records. The program's acceptance decisions reflect its configured and implemented rules, not independent confirmation that the underlying business data is correct.

## Example results

A reproducible synthetic dataset containing 1,000 customer records produced:

| Metric | Result |
|---|---:|
| Input records | 1,000 |
| Accepted records | 871 |
| Flagged records | 129 |
| Acceptance rate | 87.1% |
| Flagged rate | 12.9% |

CSV and Excel inputs produced identical acceptance counts.

## Testing

Run:

```bash
python -m pytest -q
```

At the time of this example run, all 74 automated tests passed.

## Current limitations

- Email validation checks basic syntax, not mailbox existence.
- Name capitalization uses simple title-case rules.
- Missing customer names are not currently rejected.
- Duplicate customer IDs are flagged according to the exercise's uniqueness assumption.
- Excel IDs already stored numerically may have lost leading zeros.
- The application has not been validated for large-scale production workloads.
- The current source-row calculation assumes a simple input structure.

## Data privacy

All included demonstration data is synthetic. Real customer information should not be committed to a public repository.

## Project status

Educational portfolio project demonstrating Python, pandas, data validation, automated testing, and command-line processing.