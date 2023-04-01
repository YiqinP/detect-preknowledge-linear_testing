
from detect import Detect
import pickle
from data_simulation_linear import Data_Simulartor_Linear

def main(name):
    detect = Detect(name)
    print('suspicious_item_ID: ', detect.detect_result.res_mid['comp_item_name'])
    print('suspicious_examinee_ID: ', detect.detect_result.res_mid['comp_ppl_id'])
    print('item-level confidence score:', detect.confidence_score.item_ratio)
    print('examinee-level confidence score:', detect.confidence_score.ppl_ratio)
    return detect

if __name__ == '__main__':

    name = 'my_data'

    """
    # simulate data if you do not have one
    
    simulated_data = Data_Simulartor_Linear(ppl_num=1000, item_num=100, ewp_rate=0.2, ci_rate=0.3, simu_distr={'dist': 1}, ci_accss=0.8)
    
    with open('all_info_'+name, 'wb') as f:
        str_ = pickle.dumps(simulated_data)
        f.write(str_)
    f.close()
    
    with open(name, 'wb') as f:
        str_ = pickle.dumps(simulated_data.simu_data)
        f.write(str_)
    f.close()
    """
    detect = main(name)
