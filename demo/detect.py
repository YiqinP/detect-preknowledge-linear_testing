
import pickle
from data_simulation_linear import Data_Simulartor_Linear
from detect_merge import DetectMerge, AfterDetectMerge
from detect_item import DetectItem, AfterDetectItem
from detect_ppl import DetectPpl, AfterDetectPpl
from confidence_score import ConfidenceScore, AfterConfidenceScore




class Detect():
    def __init__(self, name):
        self.name = name
        with open(name, 'rb') as f:
            self.data = pickle.loads(f.read())
        f.close()

    def process(self):
        self.ppl_result = self.ppl_detect()
        self.item_result = self.item_detect()
        self.detect_result = self.detect()
        self.confidence_score = self.confidence_score()
        return

    def item_detect(self):
        experiment = DetectItem(self.data)
        experiment.process()
        after_experiment = AfterDetectItem(experiment)
        self.save_result('item_result_' + self.name, after_experiment)
        return after_experiment

    def ppl_detect(self):
        experiment = DetectPpl(self.data)
        experiment.process()
        after_experiment = AfterDetectPpl(experiment)
        self.save_result('ppl_result_' + self.name, after_experiment)
        return after_experiment

    def detect(self):
        experiment = DetectMerge(self.data, self.ppl_result, self.item_result)
        experiment.process()
        after_experiment = AfterDetectMerge(experiment)
        self.save_result('detect_result_' + self.name, after_experiment)
        return after_experiment

    def confidence_score(self):
        experiment = ConfidenceScore(self.data, self.detect_result)
        experiment.process()
        after_experiment = AfterConfidenceScore(experiment)
        self.save_result('confidence_score_' + self.name, after_experiment)
        return after_experiment

    def save_result(self, file_name, object_name):
        with open(file_name, 'wb') as f:
            str_ = pickle.dumps(object_name)
            f.write(str_)
        f.close()


