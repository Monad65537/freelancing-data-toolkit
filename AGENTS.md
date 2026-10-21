
# AGENTS.md — Freelancing Data Toolkit

## 1. Project Purpose

This repository contains reusable Python tools for
professional Excel/CSV data processing services.

Primary service categories:
- Data cleaning and standardization
- CSV and Excel file transformation
- Dataset validation and quality assurance
- Multi-file consolidation
- Spreadsheet reporting and automation

The initial priority is reliable CSV/Excel cleaning.
Other capabilities will be implemented incrementally.

The intended users are freelancers processing
small-business datasets.

## 2. Technology Stack

- Python: 3.12
- Package and environment manager: uv
- Data processing: pandas
- Excel support: openpyxl
- Testing: pytest
- Linting and formatting: Ruff
- Version control: Git

Do not introduce additional dependencies unless
they are necessary and explicitly approved.

## 3. Core Engineering Principles

### 3.1 Correctness

Correctness takes priority over implementation speed.

- Never silently discard rows or columns.
- Never silently change data types.
- Preserve leading zeros in identifiers.
- Preserve original data unless explicitly instructed.
- Make missing-value handling explicit.
- Detect ambiguous or duplicate column names.
- Avoid unnecessary floating-point conversions.
- Use deterministic transformations where possible.
- Never claim correctness without verification.

### 3.2 Data Safety

Treat all client-provided datasets as confidential.

- Never modify or overwrite original input files.
- Write transformed results to separate output files.
- Do not upload client data to external services.
- Do not log confidential dataset contents.
- Never commit client data, credentials, or secrets.
- Use synthetic datasets for tests and demonstrations.
- Validate paths before writing output files.
- Require explicit approval for destructive operations.

### 3.3 Code Quality

- Follow Python 3.12 conventions.
- Use type hints for public functions.
- Write concise, meaningful docstrings.
- Prefer readable, maintainable code.
- Keep functions focused on one responsibility.
- Avoid unnecessary abstractions.
- Separate file I/O from data transformations.
- Handle errors explicitly.
- Avoid broad exception handling.
- Do not suppress warnings without justification.

### 3.4 Project Architecture

Organize the project as follows:

- src/data_toolkit/cleaner.py:
  Data cleaning and standardization.

- src/data_toolkit/validation.py:
  Dataset validation and quality checks.

- src/data_toolkit/consolidator.py:
  Multi-file consolidation.

- src/data_toolkit/reporter.py:
  Report generation and summaries.

- tests/:
  Automated pytest tests.

- examples/input/:
  Synthetic example input datasets.

- examples/expected/:
  Expected example outputs.

- docs/:
  Requirements and technical documentation.

Do not introduce additional modules or restructure
the project without a clear justification.

## 4. AI Agent Operating Procedure

For every implementation task:

1. Read this AGENTS.md file.
2. Read relevant specifications in docs/.
3. Identify the exact requested behavior.
4. Identify ambiguities and edge cases.
5. Ask for clarification when requirements are
   materially ambiguous.
6. Prefer the smallest correct implementation.
7. Modify only files relevant to the task.
8. Write or update automated tests.
9. Run applicable quality checks.
10. Review changes for unintended side effects.
11. Summarize implementation and test results.
12. Report limitations and unresolved risks.

Do not implement unrelated features.

Do not independently expand project scope.

Do not commit or push changes unless explicitly
instructed by the user.

## 5. Testing Requirements

Use pytest for automated testing.

Test applicable cases including:

- Normal inputs
- Empty datasets
- Missing values
- Duplicate column names
- Unexpected data types
- Whitespace inconsistencies
- Preservation of row and column counts
- Preservation of original values
- Preservation of leading zeros
- Invalid inputs and expected exceptions
- Non-mutation of source data

Every new feature must have relevant tests.

Tests must verify behavior, not merely successful
execution.

Never modify tests solely to conceal an
implementation defect.

## 6. Verification Commands

Use these commands from the repository root:

    uv run pytest -v
    uv run ruff check .
    uv run ruff format --check .

If formatting changes are needed:

    uv run ruff format .

After making corrections, rerun relevant checks.

Report actual command results.

If a command cannot be executed, explain why.
Never invent test results.

## 7. Dependency Management

Use uv exclusively for project dependencies.

Add runtime dependencies with:

    uv add PACKAGE_NAME

Add development dependencies with:

    uv add --dev PACKAGE_NAME

Execute Python with:

    uv run python

Do not install project packages globally.

Keep pyproject.toml and uv.lock synchronized.

Do not change dependency versions without
a justified reason.

## 8. Git and Change Management

- Keep changes small and reviewable.
- Preserve unrelated user modifications.
- Never use destructive Git commands without approval.
- Do not commit generated caches or virtual environments.
- Do not commit confidential client datasets.
- Do not automatically create commits.
- Do not push to remote repositories without approval.
- Explain significant modifications before completion.

## 9. Communication Requirements

When reporting completed work, use this structure:

### Changes
Describe modified files and implemented behavior.

### Verification
List commands executed and their actual results.

### Limitations
Identify unsupported cases and unresolved issues.

### Next Steps
Suggest only the next relevant development action.

Be concise, technically precise, and transparent.

Distinguish verified facts from assumptions.

## 10. Current Development Scope

Current phase: Day 1 — Environment and Foundation.

The first implementation task is:

Feature 001 — Column Name Normalization.

Requirements are defined in:

    docs/requirements.md

Do not implement file consolidation, reporting,
advanced cleaning pipelines, or unrelated features
during this phase.

Wait for explicit instructions before beginning
implementation work.
