from libraries import pd, yf
from data_processing import download_prices


class Companies:

    def __init__(self, tickers, interval="1y"):

        self.tickers = [t.upper() for t in tickers]
        self.interval = interval

        self._prices = None
        self._income_stmt = {}
        self._balance_sheet = {}
        self._cashflow = {}

    # ---------- Prices ----------        
    
    @property
    def prices(self):
        if self._prices is None:
            self._prices = download_prices(self.tickers, self.interval)
        return self._prices

    # ---------- Financial Statements ----------


    
    @property
    def income_statements(self):

        if not self._income_stmt:

            for t in self.tickers:

                try:
                    ticker = yf.Ticker(t)

                    # ---------- Annual ----------
                    annual = ticker.income_stmt

                    # ---------- Quarterly ----------
                    quarterly = ticker.quarterly_income_stmt

                    if quarterly is not None and not quarterly.empty:

                        # construir TTM
                        ttm = quarterly.iloc[:, :4].sum(axis=1)

                        # convertir a dataframe
                        ttm = pd.DataFrame(
                            ttm,
                            columns=["TTM"]
                        )

                        # unir annual + TTM
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
                    ticker = yf.Ticker(t)
                    self._balance_sheet[t] = ticker.balance_sheet
                except Exception:
                    self._balance_sheet[t] = None

        return self._balance_sheet


    @property
    def cashflows(self):

        if not self._cashflow:

            for t in self.tickers:
                try:
                    ticker = yf.Ticker(t)
                    self._cashflow[t] = ticker.cashflow
                except Exception:
                    self._cashflow[t] = None

        return self._cashflow
    
    @property
    def market_data(self):

        if not hasattr(self, "_market_data"):

            self._market_data = {}

            for t in self.tickers:
                try:
                    ticker = yf.Ticker(t)
                    info = ticker.info

                    self._market_data[t] = {
                        "market_cap": info.get("marketCap"),
                        "shares_outstanding": info.get("sharesOutstanding"),
                        "sector": info.get("sector"),
                        "industry": info.get("industry")
                    }

                except Exception:
                    self._market_data[t] = None

        return self._market_data
    
    @property
    def sectors(self):

        return {
            t: self.market_data[t]["sector"]
            for t in self.tickers
            if self.market_data[t] is not None
        }
        
    @property
    def industries(self):

        return {
            t: self.market_data[t]["industry"]
            for t in self.tickers
            if self.market_data[t] is not None
        }
        
    
