# friendly-garbanzo

A minimal example project demonstrating a simple web scraper.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the scraper with the default settings:

```bash
python src/main.py
```

The command writes the scraped data to `output/data.csv`.
Use `--output` to choose a different file and `--delay` to pause between requests:

```bash
python src/main.py --output results.csv --delay 1
```

## Customizing targets

Modify `TARGET_URLS` in `src/scraping/scraper.py` to scrape different pages.
Selectors in `SCRAPE_CONFIG` control which fields are extracted from each page.
