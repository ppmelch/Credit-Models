from libraries import pd, yf , np
from data_processing import download_prices



class Companies:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(self, tickers, interval="1y"):

        self.tickers = [t.upper() for t in tickers]
        self.interval = interval

        self._prices = None
        self._income_stmt = {}
        self._balance_sheet = {}
        self._cashflow = {}
        self._market_data = {}

        # cache yf objects
        self._yf = {
            t: yf.Ticker(t)
            for t in self.tickers
        }

    # =====================================================
    # INTERNAL RESOLVER (CORE)
    # =====================================================
    def _resolve(self, series, names, ticker):

        for n in names:
            if n in series.index:
                return series.loc[n]

        raise KeyError(
            f"{ticker} → Missing {names}"
        )

    # =====================================================
    # PRICES
    # =====================================================
    @property
    def prices(self):

        if self._prices is None:
            self._prices = download_prices(
                self.tickers,
                self.interval
            )

        return self._prices

    # =====================================================
    # RAW FINANCIAL STATEMENTS
    # =====================================================
    @property
    def income_statements(self):

        if not self._income_stmt:

            for t in self.tickers:

                try:
                    ticker = self._yf[t]

                    annual = ticker.income_stmt
                    quarterly = ticker.quarterly_income_stmt

                    if quarterly is not None and not quarterly.empty:

                        ttm = quarterly.iloc[:, :4].sum(axis=1)
                        ttm = pd.DataFrame(ttm, columns=["TTM"])

                        income = pd.concat(
                            [ttm, annual],
                            axis=1
                        )
                    else:
                        income = annual

                    self._income_stmt[t] = income

                except Exception:
                    self._income_stmt[t] = None

        return self._income_stmt


    @property
    def balance_sheets(self):

        if not self._balance_sheet:

            for t in self.tickers:
                try:
                    self._balance_sheet[t] = \
                        self._yf[t].balance_sheet
                except Exception:
                    self._balance_sheet[t] = None

        return self._balance_sheet


    @property
    def market_data(self):

        if not self._market_data:

            for t in self.tickers:

                try:
                    info = self._yf[t].info

                    self._market_data[t] = {
                        "market_cap": info.get("marketCap"),
                        "shares_outstanding": info.get("sharesOutstanding"),
                        "sector": info.get("sector"),
                        "industry": info.get("industry")
                    }

                except Exception:
                    self._market_data[t] = None

        return self._market_data

    # =====================================================
    # SHORTCUTS
    # =====================================================
    def _bs(self, ticker):
        bs = self.balance_sheets.get(ticker)
        if bs is None or bs.empty:
            raise ValueError(f"{ticker}: Balance sheet unavailable")
        return bs.iloc[:, 0]
    
    def _inc(self, ticker):

        inc = self.income_statements.get(ticker)

        if inc is None or inc.empty:
            raise ValueError(f"{ticker}: Income statement unavailable")

        if "TTM" not in inc.columns:
            raise ValueError(f"{ticker}: Missing TTM data")

        return inc["TTM"]
    # =====================================================
    # ===== FINANCIAL VARIABLES API ====
    # =====================================================

    def total_assets(self, ticker):

        return self._resolve(
            self._bs(ticker),
            ["Total Assets", "TotalAssets"],
            ticker
        )

    def total_liabilities(self, ticker):

        return self._resolve(
            self._bs(ticker),
            [
                "Total Liabilities",
                "Total Liab",
                "Total Liabilities Net Minority Interest"
            ],
            ticker
        )

    def total_debt(self, ticker):

        bs = self._bs(ticker)

        short_debt = 0
        long_debt = 0

        if "Short Long Term Debt" in bs.index:
            short_debt = bs.loc["Short Long Term Debt"]

        if "Long Term Debt" in bs.index:
            long_debt = bs.loc["Long Term Debt"]

        return short_debt + 0.5 * long_debt

    def current_assets(self, ticker):

        return self._resolve(
            self._bs(ticker),
            ["Current Assets"],
            ticker
        )

    def current_liabilities(self, ticker):

        return self._resolve(
            self._bs(ticker),
            ["Current Liabilities"],
            ticker
        )

    def retained_earnings(self, ticker):

        return self._resolve(
            self._bs(ticker),
            ["Retained Earnings"],
            ticker
        )

    def working_capital(self, ticker):

        return (
            self.current_assets(ticker)
            - self.current_liabilities(ticker)
        )

    def ebit(self, ticker):

        return self._resolve(
            self._inc(ticker),
            ["EBIT", "Operating Income"],
            ticker
        )

    def sales(self, ticker):
        return self._resolve(
            self._inc(ticker),
            ["Total Revenue", "Revenue"],
            ticker
        )

    def market_equity(self, ticker):
        return self.market_data[ticker]["market_cap"]
    
    def equity_value(self, ticker):
        return self.market_equity(ticker)
    
        
    def equity_volatility(self, ticker):
        prices = self.prices[ticker]["Adj Close"]
        returns = np.log(prices / prices.shift(1)).dropna()
        return returns.std() * np.sqrt(252)

    def sector(self, ticker):
        return self.market_data[ticker]["sector"]

    def industry(self, ticker):
        return self.market_data[ticker]["industry"]