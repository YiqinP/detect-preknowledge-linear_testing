
import numpy as np
import tensorflow as tf


class ConfidenceScore:

    def __init__(self, data,  detect_res):

        self.flagged = detect_res.res_mid
        self.nn_ppl = np.where(detect_res.count_ppl!=0)[0]

        self.resp = data['rep'].astype('float')
        
        self.ppl_num, self.item_num = self.resp.shape

        self.reduce_node_num, self.middle_node_num = 10, 50


    def process(self):
        self.nn_model()
        self.fit_check()


    def nn_model(self):

        def my_leaky_relu(x):
            return tf.nn.leaky_relu(x, alpha=0.2)

        "training"
        ac, cur_node_num, nodes_nums = my_leaky_relu, self.item_num - self.reduce_node_num, [self.item_num]
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(units=cur_node_num, input_dim=self.item_num, activation=ac))
        while cur_node_num > self.middle_node_num:
            nodes_nums.append(cur_node_num)
            cur_node_num -= self.reduce_node_num
            self.model.add(tf.keras.layers.Dense(units=cur_node_num, activation=ac))
        nodes_nums.reverse()
        for cur_node_num in nodes_nums:
            self.model.add(tf.keras.layers.Dense(units=cur_node_num, activation=ac))
        self.model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse')

        x_train, y_train = np.delete(self.resp, self.nn_ppl, axis=0), np.delete(self.resp, self.nn_ppl, axis=0)
        self.model.fit(x_train, y_train, epochs=300, verbose=0)

        "prediction"
        self.nn_pred_prob = self.model.predict(self.resp)

    def fit_check(self):

        """ This is the function for post check"""

        self.nn_pred_resp_05 = 1 * (self.nn_pred_prob > 0.5)
        self.dif_nn = np.round(np.mean(abs(self.resp - self.nn_pred_resp_05)), 3)

        "calculate item index and ppl index"

        tmp = 1 * (self.nn_pred_resp_05 < self.resp)

        count_nn_1 = np.mean(tmp[self.flagged['comp_ppl_id'], :])
        count_nn_2 = np.mean(np.delete(tmp, self.flagged['comp_ppl_id'], 0))
        self.ppl_ratio = ((count_nn_1+0.2) / (count_nn_2+0.2)) if count_nn_2<0.01 else (count_nn_1 / count_nn_2)

        count_nn_1 = np.mean(tmp[:, self.flagged['comp_item_name']])
        count_nn_2 = np.mean(np.delete(tmp, self.flagged['comp_item_name'], 1))
        self.item_ratio = ((count_nn_1+0.2) / (count_nn_2+0.2)) if count_nn_2<0.01 else (count_nn_1 / count_nn_2)



class AfterConfidenceScore:

    def __init__(self, experiment):

        self.nn_pred_prob = experiment.nn_pred_prob
        self.dif_nn = experiment.dif_nn
        self.ppl_ratio = experiment.ppl_ratio
        self.item_ratio = experiment.item_ratio
