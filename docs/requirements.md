
# Feature 001 — Column Name Normalization

## 1. Objective

Implement a reliable Python function that normalizes
pandas DataFrame column names without modifying
the original dataset.

## 2. Function Interface

Module: src/data_toolkit/cleaner.py

Function:

    normalize_column_names(
        df: pandas.DataFrame
    ) -> pandas.DataFrame

## 3. Functional Requirements

FR-001: Accept a pandas DataFrame as input.

FR-002: Return a new DataFrame without modifying
the original DataFrame.

FR-003: Remove leading and trailing whitespace
from column names.

FR-004: Convert column names to lowercase.

FR-005: Replace sequences of one or more whitespace
characters with a single underscore.

FR-006: Preserve the original column order.

FR-007: Preserve all rows and cell values.

FR-008: Preserve original data types.

FR-009: Raise ValueError if normalization produces
duplicate column names.

FR-010: Raise TypeError if any column name is not
a string.

FR-011: Support DataFrames with zero rows or
zero columns.

FR-012: Do not perform any file I/O.

## 4. Normalization Examples

Input column names:

    " Customer ID "
    "First Name"
    " Total  Amount "
    "EMAIL Address"

Expected output:

    "customer_id"
    "first_name"
    "total_amount"
    "email_address"

## 5. Duplicate Detection

Input:

    "Customer ID"
    "customer_id"

Both normalize to:

    "customer_id"

Expected behavior:

Raise ValueError with an informative message.

Do not silently rename, remove, or merge columns.

## 6. Data Integrity

The function must not:

- Delete rows or columns.
- Change cell values.
- Convert identifier strings to numbers.
- Change column order.
- Modify the input DataFrame.
- Write or overwrite any files.

## 7. Automated Tests

Implement pytest tests covering:

1. Standard column normalization.
2. Leading and trailing whitespace.
3. Multiple internal whitespace characters.
4. Uppercase and mixed-case names.
5. Duplicate normalized column names.
6. Non-string column names.
7. Empty DataFrames.
8. Preservation of row and column counts.
9. Preservation of cell values and data types.
10. Non-mutation of the input DataFrame.

## 8. Acceptance Criteria

The feature is complete only when:

- All functional requirements are satisfied.
- All relevant pytest tests pass.
- Ruff linting passes.
- Ruff formatting checks pass.
- No unrelated modules are modified.
- The implementation is reviewed by the user.

## 9. Scope Restrictions

Do not implement:

- CSV or Excel file reading/writing.
- Missing-value cleaning.
- Duplicate-row removal.
- File consolidation.
- Report generation.
- Additional transformation features.

Implement only column-name normalization.
