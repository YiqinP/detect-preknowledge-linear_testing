
import numpy as np
import pickle
import sys
sys.path.append('../data_simulation/simulation_code')
sys.path.append('../detection/merge')
sys.path.append('..')
from data_simulation_linear import Data_Simulartor_Linear
from experiment_merge import AfterExperimentMerge
from parameter import *
from experiment_follow_up import ExperimentFollowUp, AfterExperimentFollowUp


def main(simu_ids, para):

    for simu_id in simu_ids:
        print(simu_id)
        for ppl_num in para['ppl_num']:
            for item_num in para['item_num']:
                for ewp_rate in para['ewp_rate']:
                    for ci_rate in para['ci_rate']:
                        for simu_distr in para['simu_distr']:
                            for ci_accss in para['ci_accss']:
                                for iterat_times in para['iterat_times']:

                                    name =str(ppl_num) + '_' + str(item_num) + '_' + str(ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(ci_accss) +'_'+ str(simu_id)
                                    with open('../data_simulation/' + name, 'rb') as f:
                                        data = pickle.loads(f.read())
                                    f.close()

                                    name =str(ppl_num) + '_' + str(item_num) + '_' + str(ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(ci_accss) + '_' +str(iterat_times)+'_'+ str(simu_id)
                                    with open('../detection/merge/object/' + name, 'rb') as f:
                                        detect_res = pickle.loads(f.read())
                                    f.close()

                                    experiment = ExperimentFollowUp(data, detect_res)
                                    experiment.process()
                                    after_experiment = AfterExperimentFollowUp(experiment)
                                    with open('object/' + name, 'wb') as f:
                                        str_ = pickle.dumps(after_experiment)
                                        f.write(str_)
                                    f.close()


    return



if __name__ == '__main__':

    simu_ids = np.arange(exp_default_para['simulation_time'])
    main(simu_ids, para)
    main(simu_ids, para_null)

