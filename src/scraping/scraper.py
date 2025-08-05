import logging
import time
from typing import Dict, Iterable, List, Optional

import requests
from bs4 import BeautifulSoup

# Default URLs to scrape. Customize as needed.
TARGET_URLS = ["https://example.com"]

# Mapping of field names to CSS selectors and extraction attributes.
SCRAPE_CONFIG = {
    "title": {"selector": "title", "attr": "text"},
    "heading": {"selector": "h1", "attr": "text"},
}

logger = logging.getLogger(__name__)


def fetch(url: str) -> Optional[str]:
    """Fetch HTML for a single URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        logger.error("Request failed for %s: %s", url, exc)
        return None


def parse(html: str) -> Dict[str, str]:
    """Parse HTML and extract fields defined in SCRAPE_CONFIG."""
    soup = BeautifulSoup(html, "html.parser")
    data: Dict[str, str] = {}
    for field, cfg in SCRAPE_CONFIG.items():
        selector = cfg.get("selector")
        attr = cfg.get("attr", "text")
        element = soup.select_one(selector) if selector else None
        if not element:
            logger.warning("Selector '%s' not found", selector)
            data[field] = ""
            continue
        if attr == "text":
            data[field] = element.get_text(strip=True)
        else:
            data[field] = element.get(attr, "")
    return data


def scrape(urls: Iterable[str] = None, delay: float = 0.0) -> List[Dict[str, str]]:
    """Scrape multiple URLs and return a list of data dictionaries."""
    results: List[Dict[str, str]] = []
    for url in urls or TARGET_URLS:
        html = fetch(url)
        if html is None:
            continue
        try:
            data = parse(html)
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Parsing failed for %s: %s", url, exc)
            continue
        data["url"] = url
        results.append(data)
        if delay:
            time.sleep(delay)
    return results
