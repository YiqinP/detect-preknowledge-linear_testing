
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as nm
import sys
sys.path.append('..')
sys.path.append('../detection/merge')
from parameter import *
# from plot import get_summary, plot_prformance


def summary_cs(res, simu_ids, para):
    for simu_id in simu_ids:
        for ppl_num in para['ppl_num']:
            for item_num in para['item_num']:
                for ewp_rate in para['ewp_rate']:
                    for ci_rate in para['ci_rate']:
                        for simu_distr in para['simu_distr']:
                            for ci_accss in [0.6]: #para['ci_accss']:
                                for iterat_times in [60]:
                                    name = str(ppl_num) + '_' + str(item_num) + '_' + str(ewp_rate) + '_' + str(
                                        ci_rate) + '_' + str(simu_distr['id']) + '_' + str(ci_accss) + '_' + str(
                                        iterat_times) + '_' + str(simu_id)

                                    # print(name)
                                    with open('../detection/merge/object/' + name, 'rb') as f:
                                        detect_res = pickle.loads(f.read())
                                    f.close()

                                    with open('object/' + name, 'rb') as f:
                                        after_experiment = pickle.loads(f.read())
                                    f.close()

                                    tmp = [simu_id, ewp_rate, ci_rate,
                                           (after_experiment.ppl_ratio + after_experiment.item_ratio) / 2,
                                           after_experiment.ppl_ratio, after_experiment.item_ratio,
                                           len(detect_res.res_mid['comp_ppl_id']),
                                           len(detect_res.res_mid['comp_item_name']),
                                           detect_res.eva_mid['false_posi_item'],
                                           detect_res.eva_mid['false_neg_item'],
                                           detect_res.eva_mid['false_posi_ppl'],
                                           detect_res.eva_mid['false_neg_ppl'],
                                           detect_res.eva_mid['precision_ppl'],
                                           detect_res.eva_mid["precision_item"]]

                                    res.append(tmp)
    return res

def plot_cs(ind1, ind2, obj, obj_name2):

    def subplot(ewp_rate, ci_rate):

        content = res_mid[(res_mid['ewp_rate'] == ewp_rate) & (res_mid['ci_rate'] == ci_rate)]
        ax1 = plt.subplot(len(para['ewp_rate']) + 1, len(para['ci_rate']), plot_row * (len(para['ci_rate'])) + plot_col)

        if ewp_rate!=0:
            d_all = plt.scatter(y=content[ind2], x=content[ind1], c=content['index'], cmap='jet', norm=norm, alpha=0.5)
            plt.xticks(np.arange(0, 1.01, 0.1))
        else:
            d_all = plt.scatter(y=content[ind2], x=[0.1] * len(content[ind2]), c=content['index'], cmap='jet', norm=norm, alpha=0.5)
            plt.xticks([])

        if obj=='ppl':
            plt.yticks(np.arange(0, 0.21, 0.04))
        else:
            plt.yticks(np.arange(0, 0.51, 0.05))

        if plot_col == 1:
            plt.title(str(ci_rate), x=-0.33, y=0.4, rotation=90, size=18)

        if plot_row == len(para['ewp_rate']):
            if plot_col != 1:
                plt.title(str(ewp_rate), x=0.5, y=-0.37, size=18)

        if plot_col == 2 and plot_row == len(para['ewp_rate']) - 1:
            if ewp_rate!=0:
                plt.title(str(0.1), x=-0.75, y=-1.61, size=18)
            else:
                plt.title(str(0.5), x=-0.75, y=-1.61, size=18)
        if ewp_rate!=0:
            plt.xlabel('FN Rate (' + obj_name2 + ')', size=15)
        plt.ylabel('FP Rate (' + obj_name2 + ')', size=15)

        return d_all


    norm = nm.Normalize(vmin=0.9, vmax=1.5)
    fig = plt.figure(figsize=(13, 15))  # constrained_layout=True
    plt.subplots_adjust(bottom=0.15, top=0.96, left=0.15, right=0.97, wspace=0.3, hspace=0.25)  # right=0.99 #
    plot_row, plot_col = 0, 1
    subplot(0.00, 0.00)
    plot_row += 1
    for ewp_rate in para['ewp_rate']:
        plot_row = 1
        for ci_rate in para['ci_rate']:
            d_all = subplot(ewp_rate, ci_rate)
            plot_row += 1
        plot_col += 1

    fig.text(x=0.25, y=0.05, s='Proportion of Examinees With Preknowledge', fontsize=22)
    fig.text(x=0.02, y=0.35, s='Proportion of Compromised Items', fontsize=22, rotation=90)

    cb = fig.colorbar(d_all, cax=fig.add_axes([0.45, 0.9, 0.4, 0.02]) , orientation='horizontal')  # fraction = 0.0001
    cb.ax.tick_params(labelsize=20)
    cb.set_label('Confidence Score', size=20)
    plt.savefig( 'plot/'+obj + '.png')
    plt.close()



if __name__ == '__main__':

    # for iterat_times in para['iterat_times']:
    #     appdix = ''
    #     summary = get_summary(iterat_times, appdix)
    #     plot_prformance('ppl', summary, iterat_times, appdix)
    #     plot_prformance('item', summary, iterat_times, appdix)
    #
    #     appdix = '_consider_number'
    #     summary = get_summary(iterat_times, appdix)
    #     plot_prformance('ppl', summary, iterat_times, appdix)
    #     plot_prformance('item', summary, iterat_times, appdix)


    para ['simu_distr'] = [{'id': 1, 'shape':'normal', 'dist': 1}]
    simu_ids = np.arange(exp_default_para['simulation_time'])

    res_mid = list()
    res_mid = summary_cs(res_mid, simu_ids, para)
    res_mid = summary_cs(res_mid, simu_ids, para_null)
    res_mid = pd.DataFrame(res_mid, columns=["simu_id", "ewp_rate", "ci_rate", 'index', 'ppl_index', 'item_index', 'ppl_num',
                                    'item_num', 'fp_item', 'fn_item', 'fp_ppl', 'fn_ppl', 'precision_ppl', "precision_item"])

    plot_cs('fn_ppl', 'fp_ppl', 'ppl', 'EWP')
    plot_cs('fn_item', 'fp_item', 'item', 'CI')
