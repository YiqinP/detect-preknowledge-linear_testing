import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../..')
from parameter import *

def get_summary(iterat_times,appdix):
    summary = {'false_neg_ppl': {}, 'false_neg_item': {}, 'false_posi_ppl': {}, 'false_posi_item': {},
                'precision_item': {}, 'precision_ppl': {}}
    # ab_type = iteration times
    for res_name_sum, res_sum in summary.items():
        tmp = pd.read_csv('result'+appdix+'/'+res_name_sum+'.csv', header=None)
        tmp.columns=["simu_id", "ppl_num", "item_num", "ewp_rate", "ci_rate", "simu_distr", "ci_access", "iterat_times",  "val"]
        summary[res_name_sum] = {'0.6_1':{},'0.8_1':{},'1.0_1':{},'0.6_1.5':{},'0.8_1.5':{},'1.0_1.5':{}}
        for res_name, res in summary[res_name_sum].items():
            tmp_s = res_name.split('_')
            simu_distr = float(tmp_s[1])
            ci_access = float(tmp_s[0])
            res['data'] = tmp[(tmp['iterat_times'] == iterat_times)  & ((tmp['simu_distr'] == simu_distr) | (tmp['simu_distr'] == 0)) & ((tmp['ci_access'] == ci_access) | (tmp['ci_access'] == 0))]
            res['std'] = res['data'].groupby(by=["ppl_num", "item_num", "ewp_rate", "ci_rate", "simu_distr", "ci_access", "iterat_times"]).std().reset_index()
            res['mean'] = res['data'].groupby(by=["ppl_num", "item_num", "ewp_rate", "ci_rate", "simu_distr", "ci_access","iterat_times"]).mean().reset_index()
            res['med'] = res['data'].groupby(by=["ppl_num", "item_num", "ewp_rate", "ci_rate", "simu_distr", "ci_access","iterat_times"]).median().reset_index()

    return summary


def plot_prformance(type, summary, iterat_times,appdix):
    para = {'ewp_rate': [0.1,0.2,0.4], 'ci_rate': [0.1,0.2,0.4]}
    ind_set = ['std','mean'] #'med'
    label_app = {'mean': '', 'std': ' SD', 'med': ' Med'}
    eval_rows = ['0.6_1','0.8_1','1.0_1','0.6_1.5','0.8_1.5','1.0_1.5']

    # plot_titles = {'0.6_1':'CI Accessbility: 0.6\nAberrance Effect Level: 1',
    #                 '0.8_1':'CI Accessbility: 0.8\nAberrance Effect Level: 1',
    #                '1.0_1':'CI Accessbility: 1.0\nAberrance Effect Level: 1',
    #                '0.6_1.5':'CI Accessbility: 0.6\nAberrance Effect Level: 1.5',
    #                '0.8_1.5':'CI Accessbility: 0.8\nAberrance Effect Level: 1.5',
    #                '1.0_1.5':'CI Accessbility: 1.0\nAberrance Effect Level: 1.5'}
    plot_titles = {'0.6_1': 'Accessibility of CI: 0.6',
                    '0.8_1':'Accessibility of CI: 0.8',
                   '1.0_1': 'Accessibility of CI: 1.0',
                   '0.6_1.5':'',
                   '0.8_1.5':'CI Accessbility: 0.8\nAberrance Effect Level: 1.5',
                   '1.0_1.5':'CI Accessbility: 1.0\nAberrance Effect Level: 1.5'}
    eval_cols = [ 'false_neg_'+type, 'false_posi_'+type, 'precision_'+type]
    for ind in ind_set:
        fig = plt.figure(figsize=(11, 19), constrained_layout=True)  # figsize=(18, 20)
        if 'EWP' in ind:
            if 'SD' in ind:
                plt.subplots_adjust(bottom=0.01, top=0.93, left= 0.12, right=0.97,wspace=0.38, hspace=0.7)
            else:
                plt.subplots_adjust(bottom=0.01, top=0.95, left= 0.12, right=0.97,wspace=0.38, hspace=0.45)
        else:
            if 'SD' in ind:
                plt.subplots_adjust(bottom=0.01, top=0.95, left= 0.12, right=0.97,wspace=0.38, hspace=0.5)
            else:
                plt.subplots_adjust(bottom=0.01, top=0.96, left= 0.12, right=0.97,wspace=0.38, hspace=0.3)

        plot_row = 0
        for eval_row in eval_rows:
            plot_ind = 1
            for eval_col in eval_cols:
                tmp = summary[eval_col][eval_row][ind]
                l1, l2, l3, l4, l5 = list(), list(), list(), list(), list()
                for ewp_rate in para['ewp_rate']:
                    for ci_rate in para['ci_rate']:
                        if ci_rate == 0.1:
                            l1.append(tmp['val'][(tmp['ewp_rate']==ewp_rate) & (tmp['ci_rate']==ci_rate)])
                        if ci_rate == 0.2:
                            l2.append(tmp['val'][(tmp['ewp_rate']==ewp_rate) & (tmp['ci_rate']==ci_rate)])
                        if ci_rate == 0.4:
                            l3.append(tmp['val'][(tmp['ewp_rate']==ewp_rate) & (tmp['ci_rate']==ci_rate)])
                ax1 = plt.subplot(len(eval_rows), len(eval_cols), plot_row*len(eval_cols)+plot_ind)

                L1, L2, L3 = plt.plot(para['ewp_rate'], l1, 'r*-', para['ewp_rate'], l2, 'bs-', para['ewp_rate'], l3, 'go-')

                if 'posi' in eval_col:
                    l0 = np.repeat(tmp['val'][(tmp['ewp_rate']==0) & (tmp['ci_rate']==0)], len(para['ewp_rate']))
                    L0, = plt.plot(para['ewp_rate'], l0, color='orange', linestyle='-', marker='x')

                if plot_row<3:
                    if 'ppl' in eval_col and 'neg' in eval_col:
                        plt.ylabel('False Negative Rate (EWP)' + label_app[ind], fontsize=15)
                    if 'item' in eval_col and 'neg' in eval_col:
                        plt.ylabel('False Negative Rate (CI)' + label_app[ind], fontsize=15)
                    if 'ppl' in eval_col and 'posi' in eval_col:
                        plt.ylabel('False Positive Rate (EWP)' + label_app[ind], fontsize=15)
                    if 'item' in eval_col and 'posi' in eval_col:
                        plt.ylabel('False Positive Rate (CI)' + label_app[ind], fontsize=15)
                    if 'ppl' in eval_col and 'precision' in eval_col:
                        plt.ylabel('Precision (EWP)' + label_app[ind], fontsize=15)
                    if 'item' in eval_col and 'precision' in eval_col:
                        plt.ylabel('Precision (CI)' + label_app[ind], fontsize=15)

                if plot_ind == 1:
                    #ax1 = plt.subplot(4, 3, (ind_ind - 1) * 3 + plot_ind)
                    # if plot_ind==1:
                    ax1.set_title(plot_titles[eval_rows[plot_row]],  fontsize=16, x=-0.38,y=-0.08, rotation=90)
                    # if plot_ind==2:
                    #     ax1.set_title('0.9', y=-0.5, fontsize=15)
                    # if plot_ind==3:
                    #     ax1.set_title('1.0', y=-0.5, fontsize=15)


                plt.xlabel('Proportion of EWP', fontsize=13)
                plt.xticks(para['ewp_rate'], fontsize=13)

                if 'posi' in eval_col:
                    if 'ppl' in eval_col:
                        # plt.yticks(np.arange(0, 0.11, 0.01), fontsize=13)
                        plt.yticks([.00, .01, .02, .03, .04, .05, .06, .07, .08, .09, .10], fontsize=13)
                    else:
                        plt.yticks([.00  , .05, .10 , .15, .20 , 0.25, .30], fontsize=13)
                else:
                    plt.yticks([.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0], fontsize=13)
                plot_ind += 1
            plot_row += 1

        fig.legend(title="Proportion of Compromised Items:", loc='upper left', frameon=False,
                   bbox_to_anchor=(0.06, 0.995),
                   title_fontsize=15)
        #fig.text(x=0.02, y=0.3, s='Compromised Item Accessibility', fontsize=17, rotation=90)
        # fig.legend(title="Compromised Item Accessibility", loc='lower left', frameon=False,
        #            bbox_to_anchor=(0.4, 0),
        #            title_fontsize=15)
        fig.legend(handles=[L1, L2, L3, L0], labels=['0.1', '0.2', '0.4', '0.0'],
                   loc='upper left',
                   ncol=7, bbox_to_anchor=(0.4, 0.997), frameon=False, fontsize=15,
                   handlelength=1.75, columnspacing=0.8, handletextpad=0.1)
        plt.savefig('plot'+appdix+'/'+type+'_'+ind+'_'+str(iterat_times) +'.png', format='png')
        plt.close()

if __name__ == '__main__':
    for iterat_times in para['iterat_times']:
            appdix = '_mid'
            summary = get_summary(iterat_times,appdix)
            plot_prformance('ppl', summary, iterat_times,appdix)
            plot_prformance('item', summary, iterat_times,appdix)

#
# import pandas as pd
#
# for iterat_times in [60]:
#     appdix = '_mid'
#     summary = get_summary(iterat_times, appdix)
#
# d = dict()
# typs = ['ppl', 'item']
# metrics = ['false_neg_', 'false_posi_', 'precision_']
# for typ in typs:
#     for matr in metrics:
#         data = pd.DataFrame()
#         data =data.append(summary[matr+typ]['0.6_1']['std'])
#         data =data.append(summary[matr+typ]['0.8_1']['std'])
#         data =data.append(summary[matr+typ]['1.0_1']['std'])
#         d[matr+typ]=data
#
# r = dict()
# for typ in typs:
#     for matr in metrics:
#         tmp = d[matr+typ]['val'][d[matr+typ]['ci_rate']==0]
#         r[matr+typ+'_null'] = [np.round(np.nanmin(tmp),3),np.round(np.nanmax(tmp),3)]
#         tmp = d[matr+typ]['val'][d[matr+typ]['ci_rate']!=0]
#         r[matr+typ]=[np.round(np.nanmin(tmp),3),np.round(np.nanmax(tmp),3)]