
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
from contract_v01 import VanillaOption

class Sde_1d:
    def __init__(self, init_state=0., drift=lambda x:0, vol=lambda x:1, drift_ratio = .0475, vol_ratio = .2):
        self.init_state = init_state
        self.drift = drift
        self.vol = vol
        self.drift_ratio = drift_ratio
        self.vol_ratio = vol_ratio
    def euler_1d_diff(self, xh_i, dt, dw):
        mu=self.drift
        sigma=self.vol
        self.euler_diff=mu(xh_i)*dt+sigma(xh_i)*dw
        return None
    
        

class Gbm_1d(Sde_1d):
    def __int__(self, init_state = 100., drift_ratio = .0475, vol_ratio = .2):
        self.init_state = init_state
        self.drift_ratio = drift_ratio
        self.vol_ratio = vol_ratio
        self.drift = lambda x: drift_ratio*x
        self.vol = lambda x: vol_ratio*x
    def bsm_price(self, vanilla_option):
        s0 = self.init_state
        sigma = self.vol_ratio
        r = self.drift_ratio
        otype = vanilla_option.otype
        k = vanilla_option.strike
        maturity = vanilla_option.maturity
        d1 = (np.log(s0 / k) + (r + 0.5 * sigma ** 2)* maturity) / (sigma * np.sqrt(maturity))
        d2 = d1 - sigma * np.sqrt(maturity)
        return otype * s0 * ss.norm.cdf(otype * d1)- otype * np.exp(-r * maturity) * k * ss.norm.cdf(otype * d2) 
    def euler(self, grid):
        xh=[]
        n=len(grid)
        h=grid[n-1]/n
        for _ in range(n):
            dw=np.random.normal(0,h,1)
            xh.append(self.init_state)
            self.euler_1d_diff(self.init_state,h,dw)
            self.init_state=self.init_state+self.euler_diff
        return xh
    def bsm_geometric_asian_price(self, otype=1, strike=110, marturity=1, num_step=4):
        m=num_step
        n=m+1
        sigma=self.vol_ratio
        S0=self.init_state
        T=marturity
        K=strike
        r=self.drift_ratio
        mu=r-0.5*sigma**2
        mu_hat=0.5*mu
        sigma_hat_s=sigma**2*(2*m+1)/(6*(m+1))
        r_hat=mu_hat+0.5*sigma_hat_s
        sigma_hat=np.sqrt(sigma_hat_s)
        if otype==1:
            option=VanillaOption(otype = 1, strike = K, maturity= T, market_price=15.)
            return float(np.exp([(r_hat-r)*T])*Gbm_1d(init_state=S0, drift_ratio=r_hat, vol_ratio=sigma_hat).bsm_price(option))
        else:
            option=VanillaOption(otype = -1, strike = K, maturity= T, market_price=15.)
            return float(np.exp([(r_hat-r)*T])*Gbm_1d(init_state=S0, drift_ratio=r_hat, vol_ratio=sigma_hat).bsm_price(option))
            

if __name__ == '__main__':
    gbm1 = Gbm_1d(init_state=10., drift_ratio=.03, vol_ratio=.25)
    grid = np.linspace(0,1,100)
    plt.figure()
    plt.title('test Gbm_1d.euler')
    plt.xlabel('time')
    plt.ylabel('state')
    for i in range(5):
        xh = gbm1.euler(grid)
        plt.plot(grid, xh)
    plt.show()
    gbm1 = Gbm_1d(init_state=100., drift_ratio=.0475, vol_ratio=.2)
    option1 = VanillaOption(otype = 1, strike = 110., maturity= 1., market_price=15.) 
    
    print('>>>>>>>>>>call value is ' + str(gbm1.bsm_price(option1)))
    option2 = VanillaOption(otype=-1, strike = 110., maturity= 1., market_price=15.)
    print('>>>>>>>>>>put value is ' + str(gbm1.bsm_price(option2)))
        
        
        
