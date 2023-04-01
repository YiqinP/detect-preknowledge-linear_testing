
import numpy as np
import warnings
from sklearn.cluster import AgglomerativeClustering
from parameter import *
warnings.filterwarnings('ignore')

class DetectPplHelper:

    def __init__(self, data):
        self.crt, self.a = data['crt'], data['a']
        self.std = np.nanstd(self.crt)
        [self.item_num, self.ppl_num] = np.shape(data['crt'])
        self.clustering_res, self.cleaned_cluster_res = list(), list()
        self.detect_res = False

    def process(self):

        self.data_a_w_id = np.concatenate([np.array(range(self.item_num)).reshape(self.item_num, 1), self.a], axis=1)
        self.recursive_cluster(cur_2groups={})
        self.group_check() # calculate aberrant items, delete the group with aberrant item less than cri
        self.vote()

    def recursive_cluster(self,cur_2groups):

        def cluster(cur_cluster_row):
            data_a = np.delete(self.data_a_w_id, 0, axis=1)[cur_cluster_row['group_ab_item'].astype(int), :]
            label = AgglomerativeClustering(n_clusters=2,linkage="complete").fit(data_a).labels_
            #label = SpectralClustering(n_clusters=2).fit(data_a).labels_
            left = {'group_ab_item': self.data_a_w_id[cur_cluster_row['group_ab_item'], 0][np.where(label == 0)].astype(int)}
            right = {'group_ab_item': self.data_a_w_id[cur_cluster_row['group_ab_item'], 0][np.where(label == 1)].astype(int)}
            return {'left': left, 'right': right}

        if len(cur_2groups) == 0:
            cur_2groups = {'root': {'group_ab_item': self.data_a_w_id[:, 0].astype(int)}}
        for cluster_id, cur_cluster_row in cur_2groups.items():
            cur_cluster_output = cluster(cur_cluster_row)
            if (len(cur_cluster_output['left']['group_ab_item']) <= exp_default_para['ab_item_size_cri']) or \
                    (len(cur_cluster_output['right']['group_ab_item']) <= exp_default_para['ab_item_size_cri']):
                self.clustering_res.append(cur_cluster_row)
            else:
                self.recursive_cluster(cur_2groups=cur_cluster_output)

    def group_check(self):
        for cur_group in self.clustering_res:
            cur_group['group_mem_id'] = np.array(np.where(np.sum(a=self.a[cur_group['group_ab_item']], axis=0) > (len(cur_group['group_ab_item']) / 2))).flatten()
            if len(cur_group['group_mem_id']) > exp_default_para['group_mem_size_cri']:
                self.cleaned_cluster_res.append(cur_group)

    def vote(self):

        if len(self.cleaned_cluster_res) == 0:
            return

        rt_ratio = list()
        for cur_group in self.cleaned_cluster_res:
            group_mem_id, group_ab_item = cur_group['group_mem_id'], cur_group['group_ab_item']
            cur_ci_ewp = np.nanmean(self.crt[group_ab_item, :][:, group_mem_id])
            cur_ci_newp = np.nanmean(np.delete(self.crt[group_ab_item, :], group_mem_id, axis=1))
            cur_nci_ewp = np.nanmean(np.delete(self.crt[:, group_mem_id], group_ab_item, axis=0))
            rt_ratio.append(((cur_nci_ewp -cur_ci_ewp) + (cur_ci_newp - cur_ci_ewp))/(2*self.std))
            # rt_ratio.append( (cur_ci_newp - cur_ci_ewp))

        if len(rt_ratio)>0 and not np.isnan(np.nanmean(rt_ratio)):

            ind = np.nanargmax(rt_ratio)
            self.detect_group = self.cleaned_cluster_res[ind]
            self.detect_res = {'comp_ppl_id': np.sort(self.detect_group['group_mem_id']),
                               'comp_item_name': np.sort(self.detect_group['group_ab_item'])}
