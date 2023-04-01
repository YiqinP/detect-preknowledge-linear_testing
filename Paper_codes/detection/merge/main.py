import numpy as np
import pickle
import copy
from experiment_helper.evaluate import evaluate
from experiment_merge import AfterExperimentMerge
import sys
sys.path.append('../../data_simulation/simulation_code')
sys.path.append('../ppl')
sys.path.append('../../..')
from Paper_codes.parameter import *




def merge_eval(self):

    self.rt, self.crt = copy.deepcopy((self.data.simu_data['rt'])), copy.deepcopy((self.data.simu_data['rt']))
    self.resp = (self.data.simu_data['rep'])
    rt_item, rt_ppl = np.nanmedian(self.rt, axis=0), np.nanmedian(self.rt,axis=1)  # hang, lie
    self.crt -= (np.repeat([rt_item], self.ppl_num, axis=0) + np.transpose(np.repeat([rt_ppl], self.item_num, axis=0)))
    self.crt_corr = copy.copy(self.crt)
    self.crt_corr[np.where(self.resp == 0)] = np.nan
    self.std = np.nanstd(self.crt)

    step1 = np.multiply(np.linspace(exp_default_para['flag_cri']['start'],exp_default_para['flag_cri']['end'],exp_default_para['flag_cri']['steps']), np.max(self.count_ppl))
    step2 = np.multiply(np.linspace(exp_default_para['flag_cri']['start'],exp_default_para['flag_cri']['end'],exp_default_para['flag_cri']['steps']), np.max(self.count_item))
    cur_max = 0

    for i in range(len(step1)):
        for ii in range(len(step2)):
            group_mem_id = np.where(self.count_ppl >= step1[i])[0]
            group_ab_item = np.where(self.count_item >= step2[ii])[0]
            cur_ci_ewp = np.nanmean(self.crt_corr[group_mem_id, :][:, group_ab_item])
            cur_ci_newp = np.nanmean(
                np.delete(self.crt_corr[group_mem_id, :], group_ab_item, axis=1))
            cur_nci_ewp = np.nanmean(
                np.delete(self.crt_corr[:, group_ab_item], group_mem_id, axis=0))
            cur = ((cur_nci_ewp - cur_ci_ewp) + (cur_ci_newp - cur_ci_ewp))#/(2 * self.std)
            if cur > cur_max:
                self.res['comp_item_name'] = group_ab_item
                self.res['comp_ppl_id'] = group_mem_id
                cur_max = cur

    self.res_mid = copy.copy(self.res)
    self.eva_mid = evaluate(self.data, self)

    return self

def main(simu_ids,para):

    result_mid = {'false_posi_item': list(), 'false_neg_item': list(),'false_posi_ppl': list(), 'false_neg_ppl': list(),
              'precision_item': list(), 'precision_ppl': list()}


    for simu_id in simu_ids:
        print(simu_id)
        for ppl_num in para['ppl_num']:
            for item_num in para['item_num']:
                for ewp_rate in para['ewp_rate']:
                    for ci_rate in para['ci_rate']:
                        for simu_distr in para['simu_distr']:
                            for ci_accss in para['ci_accss']:

                                name = '../../data_simulation/' + str(ppl_num) + '_' + str(item_num) + '_' + str(
                                    ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(
                                    ci_accss) + '_' + str(simu_id)
                                with open(name, 'rb') as f:
                                    data = pickle.loads(f.read())
                                f.close()

                                for iterat_times in para['iterat_times']:
                                    loc = '../ppl/object/' + str(ppl_num) + '_' + str(item_num) + '_' + str(
                                           ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(ci_accss) + '_' +str(iterat_times)+'_'+ str(simu_id)
                                    with open(loc, 'rb') as f:
                                        ppl= pickle.loads(f.read())
                                    f.close()

                                    loc = '../item/object/' + str(ppl_num) + '_' + str(item_num) + '_' + str(
                                        ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(
                                        ci_accss) + '_' + str(iterat_times) + '_' + str(simu_id)
                                    with open(loc, 'rb') as f:
                                        self = pickle.loads(f.read())
                                    f.close()

                                    self.count_ppl = ppl.count_ppl
                                    self.data = data
                                    self.res = {'comp_item_name': [], 'comp_ppl_id': []}
                                    self.ppl_num, self.item_num = ppl_num, item_num

                                    experiment = merge_eval(self)
                                    after_experiment = AfterExperimentMerge(experiment)

                                    loc = 'object/' + str(ppl_num) + '_' + str(item_num) + '_' + str(
                                           ewp_rate) + '_' + str(ci_rate) + '_' + str(simu_distr['id']) + '_' + str(ci_accss) + '_' +str(iterat_times)+'_'+ str(simu_id)
                                    with open(loc, 'wb') as f:
                                        str_ = pickle.dumps(after_experiment)
                                        f.write(str_)
                                    f.close()

    #
    #                                 for false_type in exp_default_para['false_type']:
    #                                     cur_res = [simu_id, ppl_num, item_num, ewp_rate, ci_rate, simu_distr['id'],
    #                                                    ci_accss, iterat_times, self.eva_mid[false_type]]
    #                                     result_mid[false_type].append(cur_res)
    #                                     with open('result_mid/' + false_type + '.csv', 'a') as f:
    #                                         np.savetxt(f, np.array(cur_res).reshape(1, 9), delimiter=',')
    #                                     f.close()
    #
    #
    # for name, content in result_mid.items():
    #     name = 'result_mid/'+name+'.npy'
    #     content = np.array(content)
    #     if exists(name):
    #         tmp = np.load(name)
    #         content = np.concatenate([tmp, content], axis=0)
    #     np.save(name, content)

    return



if __name__ == '__main__':

    simu_ids = np.arange(exp_default_para['simulation_time'])
    main(simu_ids, para)
    main(simu_ids, para_null)
