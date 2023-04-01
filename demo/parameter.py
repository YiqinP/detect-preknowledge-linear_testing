

simu_default_para = {
    'group_num': 5,
    'rand_guess_para': {'rate_ppl': 0.1, 'rt': 2.2, 'acc': 0.25, 'dist': 0.6, 'gamma':[20, 0.5]},
    'prek_acc':0.9,
    'mu_theta': [0, 0],
    'cov_theta': [[0.097, 0.020], [0.020, 0.029]],
    'cov_item': [[0.184, -0.092, 0.009, -0.008], [-0.092, 0.276, 0.004, 0.087], [0.009, 0.004, 0.064, 0.034], [-0.008, 0.087, 0.034, 0.101]],
    'mu_item': [1.09, -0.721, 2.056, 4.006]
}



exp_default_para = {
    'iterat_prop':0.9,
    'group_mem_size_cri':5,
    'ab_item_size_cri':3,
    'flag_cri':{'start':0.5, 'end':0.7,'steps':21},
    'confidence_score_cri':1,
    'iterat_times' : 30

}

