from libraries import pd, dt, yf, re, rd


def download_prices(tickers, intervalo="5y"):

    m = re.match(r"^\s*(\d+)\s*([dwmy])\s*$", intervalo.lower())
    if not m:
        raise ValueError("Interval must follow '<int><unit>'")

    n, u = m.groups()
    delta = {"d": "days", "w": "weeks", "m": "months", "y": "years"}[u]

    start = dt.date.today() - rd(**{delta: int(n)})
    end = dt.date.today() + dt.timedelta(days=1)

    if isinstance(tickers, str):
        tickers = [tickers]

    df = yf.download(
        tickers,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df = df["Close"]
    else:
        df = df[["Close"]]

    df.index.name = "Date"

    return df.dropna(how="all")