from libraries import pd
from risk_models import RiskModel


class Altman(RiskModel):

    def __init__(self, companies):
        super().__init__(companies)

    # =====================================================
    # SAFE FINANCIAL ITEM ACCESS
    # =====================================================
    def _get_item(self, series, possible_names, ticker):

        for name in possible_names:
            if name in series.index:
                return series[name]

        available = list(series.index)

        raise KeyError(
            f"""
            Missing financial item

            Ticker: {ticker}
            Tried names: {possible_names}

            Available items:
            {available}
            """
                    )

    # =====================================================
    # SELECT ALTMAN MODEL
    # =====================================================
    def _select_model(self, ticker):

        sector = self.companies.sector(ticker)
        industry = self.companies.industry(ticker)

        manufacturing = {
            "Industrials",
            "Basic Materials",
            "Energy"
        }

        PAYMENT_KEYWORDS = [
            "Credit",
            "Payment",
            "Processing",
            "Exchange",
            "Transaction"
        ]

        # ---- Financial firms exclusion
        if sector == "Financial Services":

            # allow payment networks
            if any(word in industry for word in PAYMENT_KEYWORDS):
                return "Z_DOUBLE_PRIME"

            return None

        if sector in manufacturing:
            return "Z"

        return "Z_DOUBLE_PRIME"

    # =====================================================
    # COMPUTE FINANCIAL RATIOS
    # =====================================================
    def _compute_ratios(self, ticker):

        fs = self.companies

        X1 = fs.working_capital(ticker) / fs.total_assets(ticker)
        X2 = fs.retained_earnings(ticker) / fs.total_assets(ticker)
        X3 = fs.ebit(ticker) / fs.total_assets(ticker)
        X4 = fs.market_equity(ticker) / fs.total_liabilities(ticker)
        X5 = fs.sales(ticker) / fs.total_assets(ticker)

        return X1, X2, X3, X4, X5


    # =====================================================
    # COMPUTE Z SCORE
    # =====================================================
    def compute(self, ticker):

        try:
            X1, X2, X3, X4, X5 = self._compute_ratios(ticker)
        except Exception as e:
            print(f"⚠️ {ticker} skipped → {e}")
            return None

        model = self._select_model(ticker)

        if model == "Z":
            z = (
                1.2*X1 +
                1.4*X2 +
                3.3*X3 +
                0.6*X4 +
                1.0*X5
            )
        elif model == "Z_PRIME":
            z = (
                0.717*X1 +
                0.824*X2 +
                0.357*X3 +
                0.579*X4 +
                0.483*X5
            )
        elif model == "Z_DOUBLE_PRIME":
            z = (
                6.56*X1 +
                3.26*X2 +
                6.72*X3 +
                1.05*X4
            )

        else:
            return None

        return z

    # =====================================================
    # RATIOS TABLE FOR PORTFOLIO
    # =====================================================
    def ratios_matrix(self):

        data = []

        for ticker in self.companies.tickers:

            try:
                X1, X2, X3, X4, X5 = self._compute_ratios(ticker)

                data.append({
                    "Ticker": ticker,
                    "X1": X1,
                    "X2": X2,
                    "X3": X3,
                    "X4": X4,
                    "X5": X5
                })

            except Exception as e:
                print(f"⚠️ Skipping {ticker}: {e}")

        return pd.DataFrame(data).set_index("Ticker")

    # =====================================================
    # COMPUTE ALL Z SCORES
    # =====================================================
    def compute_all(self):

        results = {}

        for ticker in self.companies.tickers:
            results[ticker] = self.compute(ticker)

        return results
    
    
    def z_scores_df(self):

        results = self.compute_all()

        df = pd.DataFrame({
            "Ticker": results.keys(),
            "Z-Score": results.values()
        })

        return df.set_index("Ticker")