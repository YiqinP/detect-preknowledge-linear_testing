
import numpy as np
import copy
import random
from detect_ppl_helper import DetectPplHelper
from parameter import *



class DetectPpl:

    def __init__(self, data):
        [self.ppl_num, self.item_num] = data['rep'].shape
        self.iterat_times, self.cur_times = exp_default_para['iterat_times'], 0
        self.data = data
        self.count_item, self.count_ppl = np.zeros(shape=(self.item_num)), np.zeros(shape=(self.ppl_num))
        self.res = {'comp_item_name': [], 'comp_ppl_id':[]}
        self.res_mid = {'comp_item_name': [], 'comp_ppl_id': []}
        self.rt = None
        self.max_num = 0


    def process(self):

        self.prepare_data()

        while self.cur_times<self.iterat_times:
            select_item = np.sort(random.sample(set(np.array(range(self.item_num))), int(self.item_num * exp_default_para['iterat_prop'])))
            detection = DetectPplHelper({'a': self.a[select_item, :], 'crt': self.crt[select_item, :]})
            detection.process()
            if detection.detect_res:
                self.count_item[select_item[detection.detect_res['comp_item_name']]] += 1
                self.count_ppl[detection.detect_res['comp_ppl_id']] += 1
            self.cur_times += 1

    def prepare_data(self):
        if self.rt is None:
            self.rt, self.crt  = copy.deepcopy(np.transpose(self.data['rt'])), copy.deepcopy(np.transpose(self.data['rt']))
            self.resp = np.transpose(self.data['rep'])
            rt_item, rt_ppl = np.nanmedian(self.rt, axis=1), np.nanmedian(self.rt, axis=0)   # hang, lie
            self.crt -= (np.repeat([rt_ppl], self.item_num, axis=0) + np.transpose(np.repeat([rt_item], self.ppl_num, axis=0)))
            self.crt_corr = copy.copy(self.crt)
            self.crt_corr[np.where(self.resp==0)] = np.nan
            self.rt_corr = copy.copy(self.rt)
            self.rt_corr[np.where(self.resp==0)] = np.nan
            self.a = (1 * (self.crt < np.nanmedian(self.crt))) * self.resp
            self.crt[np.where(self.a==0)],self.rt[np.where(self.a == 0)] = np.nan, np.nan
            self.std = np.nanstd(self.crt)



class AfterDetectPpl:

    def __init__(self, experiment):
        self.count_ppl = experiment.count_ppl
        self.count_item = experiment.count_item
