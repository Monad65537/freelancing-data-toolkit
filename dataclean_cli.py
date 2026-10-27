
import argparse
import logging
from pathlib import Path

from dataclean_pro.cleaner import clean_data, load_data
from dataclean_pro.report import (
    generate_report,
    save_report,
    save_results,
)
from dataclean_pro.validator import validate_data

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Clean and validate customer datasets."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input CSV or XLSX file.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Directory for generated files.",
    )

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=output_dir / "execution.log",
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
        force=True,
    )

    logger.info("Loading input dataset")

    df = load_data(args.input)
    logger.info("Input rows: %d", len(df))

    cleaned = clean_data(df)
    logger.info("Cleaning completed")

    accepted, flagged = validate_data(cleaned)
    logger.info("Accepted rows: %d", len(accepted))
    logger.warning("Flagged rows: %d", len(flagged))

    report = generate_report(accepted, flagged)

    save_results(accepted, flagged, output_dir)
    save_report(
        report,
        output_dir / "quality_report.json",
    )

    logger.info("Results exported successfully")

    print("Processing completed.")
    print(f"Input rows: {report['input_rows']}")
    print(f"Accepted rows: {report['accepted_rows']}")
    print(f"Flagged rows: {report['flagged_rows']}")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    main()
