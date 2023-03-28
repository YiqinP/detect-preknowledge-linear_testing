

import numpy as np
import copy
import random
from experiment_helper.detect_item import DetectorItem
import sys
sys.path.append('../..')
from parameter import *



class ExperimentItem:

    def __init__(self, ppl_num, item_num, ewp_rate, ci_rate, iterat_times, data):
        #self.ppl_num, self.item_num, self.ewp_rate, self.ci_rate = ppl_num, item_num, ewp_rate, ci_rate
        self.item_num, self.ppl_num, self.ci_rate, self.ewp_rate = item_num, ppl_num, ci_rate, ewp_rate
        self.iterat_times, self.cur_times = iterat_times, 0
        self.data = data
        self.count_item, self.count_ppl = np.zeros(shape=(self.item_num)), np.zeros(shape=(self.ppl_num))
        self.res = {'comp_item_name': [], 'comp_ppl_id':[]}
        self.res_mid = {'comp_item_name': [], 'comp_ppl_id': []}
        self.rt = None
        self.max_num = 0


    def process(self):

        self.prepare_data()

        while self.cur_times<self.iterat_times:
            select_ppl = np.sort(random.sample(set(np.array(range(self.ppl_num))), int(self.ppl_num * exp_default_para['iterat_prop'])))
            detection = DetectorItem({'a': self.a[select_ppl, :], 'crt': self.crt[select_ppl, :]})
            detection.process()
            if detection.detect_res:
                self.count_item[detection.detect_res['comp_item_name']] += 1
                self.count_ppl[select_ppl[detection.detect_res['comp_ppl_id']]] += 1
            self.cur_times += 1


    def prepare_data(self):
        # center rt
        if self.rt is None:
            self.rt, self.crt  = copy.deepcopy((self.data.simu_data['rt'])), copy.deepcopy((self.data.simu_data['rt']))
            self.resp = (self.data.simu_data['rep'])
            rt_item, rt_ppl = np.nanmedian(self.rt, axis=0), np.nanmedian(self.rt, axis=1)   # hang, lie
            self.crt -= ( np.repeat([rt_item], self.ppl_num, axis=0)+ np.transpose(np.repeat([rt_ppl], self.item_num, axis=0)))
            self.crt_corr = copy.copy(self.crt)
            self.crt_corr[np.where(self.resp==0)] = np.nan
            self.rt_corr = copy.copy(self.rt)
            self.rt_corr[np.where(self.resp==0)] = np.nan
            self.a = (1 * (self.crt < np.nanmedian(self.crt))) * self.resp
            self.crt[np.where(self.a==0)],self.rt[np.where(self.a == 0)] = np.nan, np.nan
            self.std = np.nanstd(self.crt)


class AfterExperimentItem:

    def __init__(self, experiment):
        self.count_ppl, self.count_item = experiment.count_ppl, experiment.count_item
