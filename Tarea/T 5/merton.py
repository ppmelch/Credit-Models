from libraries import norm, np , pd
from risk_models import RiskModel


class Merton(RiskModel):

    def __init__(self, companies, rf=0.03):
        super().__init__(companies)
        self.rf = rf

    def V(self, ticker):
        return self.companies.market_equity(ticker) + self.companies.total_debt(ticker)

    def D(self, ticker):
        return self.companies.total_debt(ticker)

    def vol(self, ticker):
        return self.companies.equity_volatility(ticker)

    def distance_to_default(self, ticker, T=1):
        V = self.V(ticker)
        D = self.D(ticker)
        sigma = self.vol(ticker)
        return (np.log(V/D) + (self.rf + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))

    def probability_of_default(self, ticker, T=1):
        DD = self.distance_to_default(ticker, T)
        return 1 - norm.cdf(DD)

    def merton_df(self):
        data = []
        for ticker in self.companies.tickers:
            try:
                dd = self.distance_to_default(ticker)
                prob_default = self.probability_of_default(ticker)
                data.append({
                    "Ticker": ticker,
                    "Distance to Default": dd,
                    "Probability of Default": prob_default
                })
            except Exception as e:
                print(f"⚠️ {ticker} skipped → {e}")
        return pd.DataFrame(data).set_index("Ticker")