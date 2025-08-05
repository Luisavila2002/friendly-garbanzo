import argparse
import csv
import logging
import os

from scraping.scraper import TARGET_URLS, scrape

logging.basicConfig(level=logging.INFO)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple web scraper")
    parser.add_argument(
        "--output", default="output/data.csv", help="Path to output CSV file"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Delay in seconds between requests",
    )
    args = parser.parse_args()

    data = scrape(TARGET_URLS, delay=args.delay)
    if not data:
        logging.warning("No data scraped")
        return

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    logging.info("Wrote %d records to %s", len(data), args.output)


if __name__ == "__main__":
    main()
