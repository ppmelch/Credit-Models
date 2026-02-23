
class RiskModel:

    def __init__(self, companies):
        self.companies = companies
        self._ratio_cache = {}

    def compute(self, ticker):
        """
        Cada modelo debe implementar esto.
        """
        raise NotImplementedError(
            "Subclasses must implement compute()"
        )
        
        
