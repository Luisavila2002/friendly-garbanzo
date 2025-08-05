import requests
import pandas as pd
from typing import List, Dict

BVC_QUOTES_URL = "https://www.bolsadecaracas.com/wp-admin/admin-ajax.php?action=get_cotizaciones"


def fetch_quotes() -> List[Dict[str, str]]:
    """Retrieve current stock quotes from Bolsa de Valores de Caracas."""
    response = requests.get(BVC_QUOTES_URL, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("response", [])


def quotes_to_dataframe(quotes: List[Dict[str, str]]) -> pd.DataFrame:
    """Convert raw quote list to a pandas DataFrame with numeric columns."""
    df = pd.DataFrame(quotes)
    for col in ["VOL_CMP_1", "PRE_CMP_1", "PRE_VTA_1", "VOL_VTA_1"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def save_quotes_csv(path: str) -> None:
    """Download quotes and save them as a CSV file."""
    quotes = fetch_quotes()
    df = quotes_to_dataframe(quotes)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch Venezuelan stock market quotes and store them as CSV.")
    parser.add_argument("--output", default="quotes.csv", help="Path to output CSV file")
    args = parser.parse_args()

    save_quotes_csv(args.output)
    print(f"Saved quotes to {args.output}")
