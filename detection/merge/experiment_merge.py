class AfterExperimentMerge:
    def __init__(self, experiment):
        self.count_ppl, self.count_item = experiment.count_ppl, experiment.count_item
        self.res_mid = experiment.res_mid
        self.eva_mid = experiment.eva_mid
