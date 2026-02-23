from data_processing import download_prices


class Market:

    def __init__(self, tickers, benchmark=None):

        self.tickers = tickers
        self.benchmark_symbol = benchmark

        self.prices = None
        self.benchmark = None

    def load_prices(self, intervalo="5y"):

        # portfolio assets
        self.prices = download_prices(
            self.tickers,
            intervalo
        )

        # benchmark
        if self.benchmark_symbol:
            bench = download_prices(
                self.benchmark_symbol,
                intervalo
            )
            
            bench = bench.iloc[:, 0]

            common_dates = self.prices.index.intersection(
                bench.index
            )

            self.prices = self.prices.loc[common_dates]
            self.benchmark = bench.loc[common_dates]

        return self.prices, self.benchmark