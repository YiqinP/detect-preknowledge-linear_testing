import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import sys
sys.path.append('../../..')
from Paper_codes.parameter import *


def moedl_fit(type):

    tmp = pd.DataFrame(np.load('result_mid/'+type+'.npy'))
    tmp.columns=["simu_id", "ppl_num", "item_num", "ewp_rate", "ci_rate", "simu_distr", "ci_access", "iterat_times",  "val"]
    tmp = tmp[(tmp['iterat_times']==30) | (tmp['iterat_times']==60) ]
    d_m = tmp[(tmp['simu_distr']==1) | (tmp['simu_distr']==1.5) ]
    model = ols('val ~ C(ewp_rate)*C(ci_rate)*C(simu_distr)*C(ci_access)*C(iterat_times)', data=d_m).fit()
    anova_table = sm.stats.anova_lm(model,typ=3)
    anova_table['partial_eta_sqr']=anova_table['sum_sq']/(anova_table['sum_sq']['Residual']+anova_table['sum_sq'])
    anova_table.to_csv('anova_result/'+type+".csv",float_format='%.3f')

for ele in exp_default_para['false_type']:
    moedl_fit(ele)
