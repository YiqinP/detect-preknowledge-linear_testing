
import numpy as np
import pickle
import sys
sys.path.append('../../data_simulation/simulation_code')
sys.path.append('../../..')
from Paper_codes.parameter import *
from experiment_item import ExperimentItem, AfterExperimentItem


def main(simu_ids,para):


    for simu_id in simu_ids:
        print(simu_id)
        for ppl_num in para['ppl_num']:
            for item_num in para['item_num']:
                for ewp_rate in para['ewp_rate']:
                    for ci_rate in para['ci_rate']:
                        for simu_distr in para['simu_distr']:
                            for ci_accss in para['ci_accss']:

                                name = '../../data_simulation/' + str(ppl_num) + '_' + str(item_num) + '_' + str(
                                       ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(ci_accss) + '_' + str(simu_id)
                                with open(name, 'rb') as f:
                                    data = pickle.loads(f.read())
                                f.close()

                                experiment = ExperimentItem(ppl_num=ppl_num, item_num=item_num, ewp_rate=ewp_rate,
                                                        ci_rate=ci_rate, iterat_times=0, data=data)

                                for iterat_times in para['iterat_times']:

                                    experiment.iterat_times = iterat_times
                                    experiment.process()

                                    after_experiment = AfterExperimentItem(experiment)
                                    loc = 'object/' + str(ppl_num) + '_' + str(item_num) + '_' + str(
                                           ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(ci_accss) + '_' +str(iterat_times)+'_'+ str(simu_id)
                                    with open(loc, 'wb') as f:
                                        str_ = pickle.dumps(after_experiment)
                                        f.write(str_)
                                    f.close()


    return



if __name__ == '__main__':

    simu_ids = np.arange(exp_default_para['simulation_time'])
    main(simu_ids, para)
    main(simu_ids, para_null)
