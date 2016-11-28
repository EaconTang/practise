# coding=utf8
from numpy import *
from math import log
import matplotlib


def calc_shannon_ent(data_set):
    """
    计算香农熵，熵越高，混合的数据越多
    """
    num_entries = len(data_set)
    label_counts = {}
    for _ in data_set:
        _label = _[-1]
        if _label not in label_counts.keys():
            label_counts[_label] = 0
        label_counts[_label] += 1
    shannon_ent = 0.0
    for key in label_counts.keys():
        prob = float(label_counts[key]) / num_entries
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent


def create_data_set():
    """返回数据集"""
    data_set = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing', 'flippers']
    return data_set, labels


def split_dataset(dataset, axis, value):
    """根据给定特征值划分数据集"""
    ret_dataset = []
    for _ in dataset:
        if _[axis] == value:
            ret_dataset.append(_[:axis] + _[axis + 1:])
    return ret_dataset


def choose_best_feature_to_split(dataset):
    """选择最好的数据集划分方式"""
    num_features = len(dataset[0]) - 1
    base_entropy = calc_shannon_ent(dataset)
    best_info_gain = 0.0
    best_feature = -1
    for i in range(num_features):
        feat_list = [_[i] for _ in dataset]
        unique_vals = set(feat_list)
        new_entropy = 0.0
        for value in unique_vals:
            sub_dataset = split_dataset(dataset, i, value)
            prob = len(sub_dataset) / float(len(dataset))
            new_entropy += prob * calc_shannon_ent(sub_dataset)
        info_gain = base_entropy - new_entropy
        if (info_gain > best_info_gain):
            best_info_gain = info_gain
            best_feature = i
    return best_feature


if __name__ == '__main__':
    data_set, labels = create_data_set()
    print choose_best_feature_to_split(data_set)
