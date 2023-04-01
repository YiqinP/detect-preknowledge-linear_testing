import numpy as np
import pickle
import sys
sys.path.append('../../..')
from Paper_codes.parameter import *
from data_simulation_linear import Data_Simulartor_Linear

def main(simu_ids, para):
    for simu_id in simu_ids:
        for ppl_num in para['ppl_num']:
            for item_num in para['item_num']:
                for ewp_rate in para['ewp_rate']:
                    for ci_rate in para['ci_rate']:
                        for simu_distr in para['simu_distr']:
                            for ci_accss in para['ci_accss']:
                                data = Data_Simulartor_Linear(ppl_num, item_num, ewp_rate, ci_rate, simu_distr, ci_accss)
                                data.simulate()
                                name = '../'+str(ppl_num) + '_' + str(item_num) + '_'+str(ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id'])+ '_' + str(ci_accss)+ '_' + str(simu_id)
                                with open(name, 'wb') as f:
                                    str_ = pickle.dumps(data)
                                    f.write(str_)
                                f.close()

simu_ids = np.arange(exp_default_para['simulation_time'])
main(simu_ids, para)
main(simu_ids, para_null)
