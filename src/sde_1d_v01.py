import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
from contract_v01 import VanillaOption
# In[2]:


'''=========
sde class init
=========='''

class Sde_1d:
    def __init__(self,
                init_state = 0.,
                drift = lambda x: 0,
                vol = lambda x: 1.
                ):
        self.init_state = init_state
        self.drift = drift
        self.vol = vol
        




'''============
Gbm class inherited from sde_1d
============='''

class Gbm_1d(Sde_1d):
    def __init__(self,
                 init_state = 100.,
                 drift_ratio = .0475,
                 vol_ratio = .2
                ):
        self.init_state = init_state
        
        self.drift_ratio = drift_ratio
        self.vol_ratio = vol_ratio
        
        self.drift = lambda x: drift_ratio*x
        self.vol = lambda x: vol_ratio*x

    def bsm_price(self, vanilla_option):
    S0 = self.init_state
    sigma = self.vol_ratio
    r = self.drift_ratio
    
    otype = vanilla_option.otype
    k = vanilla_option.strike
    maturity = vanilla_option.maturity
    
    d1 = (np.log(S0 / k) + (r + 0.5 * sigma ** 2) 
          * maturity) / (sigma * np.sqrt(maturity))
    d2 = d1 - sigma * np.sqrt(maturity)
    
    return (otype * S0 * ss.norm.cdf(otype * d1) #line break needs parenthesis
            - otype * np.exp(-r * maturity) * k * ss.norm.cdf(otype * d2))

   Gbm_1d.bsm_price = bsm_price     

    def bsm_geometric_asian_price(self,
    otype = 1,
    strike = 110.,
    maturity = 1,
     num_step = 4 #patition number
     ):
    m=num_step
    n=m+1
    r=self.drift_ratio
    sigma=self.vol_ratio
    S0=self.init_state
    T=marturity
    K=strike
    mu=r-0.5*sigma**2
    mu_hat=0.5*mu
    sigma_hat_square=sigma**2*(2*m+1)/(6*(m+1))
    sigma_hat=np.sqrt(sigma_hat_square)
    r_hat=mu_hat+0.5*sigma_hat_square
        if otype==1:
            option=VanillaOption(otype = 1, strike = K, maturity= T, market_price=15.)
            return float(np.exp([(r_hat-r)*T])*Gbm_1d(init_state=S0, drift_ratio=r_hat, vol_ratio=sigma_hat).bsm_price(option))
        else:
            option=VanillaOption(otype = -1, strike = K, maturity= T, market_price=15.)
            return float(np.exp([(r_hat-r)*T])*Gbm_1d(init_state=S0, drift_ratio=r_hat, vol_ratio=sigma_hat).bsm_price(option))

    Gbm_1d.bsm_geometric_asian_price = bsm_geometric_asian_price









# In[5]:

if __name__ == '__main__':       

        
            
    '''===============
    Test bsm_price
    ================='''
    gbm1 = Gbm_1d(init_state=100., drift_ratio=.0475, vol_ratio=.2)
    option1 = VanillaOption(otype = 1, strike = 110., maturity= 1., market_price=15.) 
    
    print('>>>>>>>>>>call value is ' + str(gbm1.bsm_price(option1)))
    option2 = VanillaOption(otype=-1)
    print('>>>>>>>>>>put value is ' + str(gbm1.bsm_price(option2)))  
