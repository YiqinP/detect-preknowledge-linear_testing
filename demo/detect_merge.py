

import copy
import numpy as np
from parameter import *

class DetectMerge:

    def __init__(self, data, ppl_result, item_result):
        [self.ppl_num, self.item_num] = data['rep'].shape
        self.data = data
        self.count_ppl = ppl_result.count_ppl
        self.count_item = item_result.count_item

        self.res = {'comp_item_name': [], 'comp_ppl_id': []}

    def process(self):
        self.rt, self.crt = copy.deepcopy((self.data['rt'])), copy.deepcopy((self.data['rt']))
        self.resp = (self.data['rep'])
        rt_item, rt_ppl = np.nanmedian(self.rt, axis=0), np.nanmedian(self.rt, axis=1)  # hang, lie
        self.crt -= (np.repeat([rt_item], self.ppl_num, axis=0) + np.transpose(
            np.repeat([rt_ppl], self.item_num, axis=0)))
        self.crt_corr = copy.copy(self.crt)
        self.crt_corr[np.where(self.resp == 0)] = np.nan
        self.std = np.nanstd(self.crt)

        step1 = np.multiply(np.linspace(exp_default_para['flag_cri']['start'], exp_default_para['flag_cri']['end'],
                                        exp_default_para['flag_cri']['steps']), np.max(self.count_ppl))
        step2 = np.multiply(np.linspace(exp_default_para['flag_cri']['start'], exp_default_para['flag_cri']['end'],
                                        exp_default_para['flag_cri']['steps']), np.max(self.count_item))
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
                cur = ((cur_nci_ewp - cur_ci_ewp) + (cur_ci_newp - cur_ci_ewp))  # /(2 * self.std)
                if cur > cur_max:
                    self.res['comp_item_name'] = group_ab_item
                    self.res['comp_ppl_id'] = group_mem_id
                    cur_max = cur

        self.res_mid = copy.copy(self.res)


class AfterDetectMerge:
    def __init__(self, experiment):
        self.count_ppl, self.count_item = experiment.count_ppl, experiment.count_item
        self.res_mid = experiment.res_mid
