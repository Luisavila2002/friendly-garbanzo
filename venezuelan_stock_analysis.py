import yfinance as yf
import pandas as pd


def fetch_ibvc_data(period: str = "1mo") -> pd.DataFrame:
    """Fetch historical data for the Caracas Stock Exchange index (IBVC)."""
    return yf.download("^IBVC", period=period)


def analyze_data(df: pd.DataFrame) -> pd.Series:
    """Compute basic statistics on closing prices."""
    closes = df["Close"].dropna()
    returns = closes.pct_change().dropna()
    stats = pd.Series({
        "mean_close": closes.mean(),
        "median_close": closes.median(),
        "std_return": returns.std(),
        "mean_return": returns.mean(),
    })
    return stats


def main() -> None:
    df = fetch_ibvc_data()
    if df.empty:
        print("No data retrieved.")
        return
    stats = analyze_data(df)
    print("IBVC statistics for the last month:")
    print(stats)


if __name__ == "__main__":
    main()
