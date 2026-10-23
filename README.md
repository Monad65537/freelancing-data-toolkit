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

Requirements:

- Python 3.12 or compatible version
- pandas
- openpyxl
- pytest (for testing)

Install dependencies:

```bash
python -m pip install pandas openpyxl pytest
```

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