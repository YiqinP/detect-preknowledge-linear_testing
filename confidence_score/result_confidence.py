import numpy as np
import pickle
import sys
sys.path.append('../detection/merge')
sys.path.append('..')
from experiment_merge import AfterExperimentMerge
from experiment_follow_up import ExperimentFollowUp, AfterExperimentFollowUp
from parameter import *

"""
The index is calculated based on only middle result
(detected ppl/item for IRT + counted flagged times for NN)
"""

def main(simu_ids, para, consider_number=False):
    for simu_id in simu_ids:
        for ppl_num in para['ppl_num']:
            for item_num in para['item_num']:
                for ewp_rate in para['ewp_rate']:
                    for ci_rate in para['ci_rate']:
                        for simu_distr in para['simu_distr']:
                            for ci_accss in para['ci_accss']:
                                for iterat_times in para['iterat_times']:

                                    name =str(ppl_num) + '_' + str(item_num) + '_' + str(ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(ci_accss) + '_' +str(iterat_times)+'_'+ str(simu_id)
                                    with open('../detection/merge/object/' + name, 'rb') as f:
                                        detect_res = pickle.loads(f.read())
                                    f.close()
                                    with open('object/' + name, 'rb') as f:
                                        after_experiment = pickle.loads(f.read())
                                    f.close()

                                    if consider_number:
                                        if_flag = (after_experiment.ppl_ratio+after_experiment.item_ratio)/2<exp_default_para['confidence_score_cri'] \
                                                  and len(detect_res.res_mid['comp_item_name'])>0.1*item_num
                                    else:
                                        if_flag = (after_experiment.ppl_ratio+after_experiment.item_ratio)/2<exp_default_para['confidence_score_cri']

                                    if if_flag:
                                        detect_res.eva_mid['false_posi_ppl'] = 0
                                        detect_res.eva_mid['false_neg_ppl'] = 1 if ewp_rate!=0 else np.nan
                                        detect_res.eva_mid['precision_ppl'] = np.nan
                                        detect_res.eva_mid['false_posi_item'] = 0
                                        detect_res.eva_mid['false_neg_item'] = 1 if ci_rate!=0 else np.nan
                                        detect_res.eva_mid['precision_item'] = np.nan


                                    for false_type in exp_default_para['false_type']:
                                        cur_res = [simu_id, ppl_num, item_num, ewp_rate, ci_rate, simu_distr['id'],
                                                       ci_accss, iterat_times, detect_res.eva_mid[false_type]]
                                        with open(('result_consider_number/' if consider_number else 'result/')+ false_type + '.csv', 'a') as f:
                                            np.savetxt(f, np.array(cur_res).reshape(1, 9), delimiter=',')
                                        f.close()
    return



if __name__ == '__main__':

    simu_ids = np.arange(exp_default_para['simulation_time'])
    main(simu_ids, para)
    main(simu_ids, para_null)
    main(simu_ids, para, consider_number=True)
    main(simu_ids, para_null, consider_number=True)
