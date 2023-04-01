import numpy as np
import scipy.stats as ss
import random
import copy
import sys
sys.path.append('../../..')
from Paper_codes.parameter import *

class Data_Simulartor_Linear:

    def __init__(self, ppl_num, item_num, ewp_rate, ci_rate, simu_distr, ci_accss):
        self.ppl_num, self.item_num, self.ewp_rate, self.ci_rate, self.ci_accss = \
            ppl_num, item_num, ewp_rate, ci_rate, ci_accss
        self.simu_distr = simu_distr
        self.group_num = simu_default_para['group_num']
        self.rand_guess_para = simu_default_para['rand_guess_para']
        self.prek_acc = simu_default_para['prek_acc']
        self.mu_theta, self.cov_theta = simu_default_para['mu_theta'], simu_default_para['cov_theta']
        self.mu_item, self.cov_item = simu_default_para['mu_item'], simu_default_para['cov_item']

    def simulate(self):
        self.simu_org_data()
        self.comp_selection()
        self.data_modify()


    def simu_org_data(self):


        theta = np.random.multivariate_normal(mean=self.mu_theta, cov=self.cov_theta, size=self.ppl_num)
        ab = np.random.multivariate_normal(mean=self.mu_item, cov=self.cov_item, size=self.item_num)

        par = ss.norm.cdf(np.dot(theta[:, 0].reshape([len(theta[:, 0]),1]), ab[:, 0].reshape([1,len(ab[:, 0])])) - np.repeat([ab[:, 1]],self.ppl_num,axis=0))
        probs = np.random.uniform(0,1,self.item_num*self.ppl_num).reshape([self.ppl_num, self.item_num])
        Y = 1*(par>probs)

        rt_base = np.zeros((self.ppl_num, self.item_num))
        for j in range(self.item_num):
            rt_base[:, j] =  np.random.normal(loc=0, scale=1/ab[j,2], size=self.ppl_num)
        RT = np.repeat([ab[:, 3]], self.ppl_num, axis=0)-np.transpose(np.repeat([theta[:, 1]],self.item_num,axis=0)) + rt_base

        # from rpy2 import robjects
        # robjects.r.source('simu.R')
        # out = robjects.r.simLnIrt(self.ppl_num, self.item_num)
        # Y = np.asarray(out.rx2('Y'))
        # RT = np.asarray(out.rx2('RT'))
        # theta = np.asarray(out.rx2('theta'))
        # ab = np.asarray(out.rx2('ab'))
        # probs = np.asarray(out.rx2('probs'))

        self.org_data = {'rep': Y, 'rt': RT, 'theta': theta, 'item_para': ab, 'probs':par}


    def comp_selection(self):

       comp_ppl_num = int(self.ewp_rate * self.ppl_num)
       comp_ppl_id = random.sample(set(np.arange(self.ppl_num)), comp_ppl_num)
       dic_ppl = dict()
       cur_group, cur_group_size = 0,0
       for ele in comp_ppl_id:
          dic_ppl[ele] = cur_group
          cur_group_size += 1
          if cur_group_size == comp_ppl_num//self.group_num:
             cur_group+=1
             cur_group_size=0

       comp_item_num = int(self.ci_rate * self.item_num)
       comp_item_name = random.sample(set(np.arange(self.item_num)), comp_item_num)
       dic_item = dict()
       for id in range(self.group_num):
          dic_item[id] = random.sample(comp_item_name,int(comp_item_num*self.ci_accss))

       self.comp = {'comp_ppl_id': comp_ppl_id, 'comp_item_name': comp_item_name, 'dic_ppl':dic_ppl, 'dic_item':dic_item}

    def data_modify(self):

        rep, rt = copy.deepcopy(self.org_data['rep']), copy.deepcopy(self.org_data['rt'])
        rt_sdt, rt_mean = np.std(rt), np.mean(rt)
        dic_ppl, dic_item = self.comp['dic_ppl'], self.comp['dic_item']
        for cur_ppl, cur_group in dic_ppl.items():
            cur_item = dic_item[cur_group]
            for ele in cur_item:
                rt[cur_ppl][ele] = np.random.normal(loc=rt_mean - rt_sdt * self.simu_distr['dist'], scale=rt_sdt, size=1)
                rep[cur_ppl][ele] = 0 if np.random.uniform(low=0, high=1, size=1) >= self.prek_acc else 1

        # simulate rapid guessing
        self.aberrant_ind = list()
        guess_ppl = np.random.choice(a=np.delete(np.arange(self.ppl_num),self.comp['comp_ppl_id']),
                                     size=int(self.ppl_num*self.rand_guess_para['rate_ppl']),
                                     replace=False)
        for gp in guess_ppl:
            guess_num = int(np.round(np.random.gamma(self.rand_guess_para['gamma'][0], self.rand_guess_para['gamma'][1], 1)[0], 0))
            if guess_num>0:
                guess_rep = np.random.binomial(n=1, p=self.rand_guess_para['acc'], size=guess_num)
                rep[gp][-guess_num:] = guess_rep
                guess_rt = np.random.normal(loc=self.rand_guess_para['rt'], scale=rt_sdt* self.rand_guess_para['dist'], size=guess_num)
                rt[gp][-guess_num:] = guess_rt
                self.aberrant_ind.append([gp, guess_num])

        self.simu_data = {'rep': rep, 'rt': rt}

