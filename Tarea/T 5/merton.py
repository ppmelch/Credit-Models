from libraries import norm, np
from risk_models import RiskModel


def merton_model(V, D, rf, vol , T):
    return (np.log(V/D) + (rf + (vol**2/2)) * T) / (vol * np.sqrt(T)) 

def merton_distance_to_default(merton_model):
    return 1 - norm.cdf(merton_model)

    
class Merton(RiskModel):
    def __init__(self, companies):
        super().__init__(companies)
        
        
    
    
    