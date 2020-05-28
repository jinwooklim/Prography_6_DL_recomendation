from math import sqrt
import numpy as np
from collections import defaultdict
from sklearn.metrics import mean_squared_error


def cosine_similarity(train_matrix, kind='user', epsilon=1e-9):
    if kind == 'user':
        sim = train_matrix.dot(train_matrix.T) + epsilon
    elif kind == 'location':
        sim = train_matrix.T.dot(train_matrix) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)


def predict(checkins, similarity, type='user'):
    if type == 'user':
        pred = similarity.dot(checkins) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = checkins.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred


def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))


def memory_based_collaborative_filtering(train_data, test_data, n_users, n_locations):
    train_data_matrix = np.zeros((n_users, n_locations))

    for checkin in train_data.itertuples():
        train_data_matrix[checkin[1], checkin[2]] = checkin[3]

    # for RMSE
    test_data_matrix = np.zeros((n_users, n_locations))

    # for precision and recall
    ground_truth_dic = defaultdict(set)

    for checkin in test_data.itertuples():
        test_data_matrix[checkin[1], checkin[2]] = checkin[3]
        ground_truth_dic[int(checkin[1])].add(int(checkin[2]))

    user_similarity = cosine_similarity(train_data_matrix)
    # item_similarity = cosine_similarity(train_data_matrix.T)

    user_prediction = predict(train_data_matrix, user_similarity, type='user')
    # item_prediction = predict(train_data_matrix, item_similarity, type='item')

    UB_RMSE = rmse(user_prediction, test_data_matrix)
    # IB_RMSE = rmse(item_prediction, test_data_matrix)
    return UB_RMSE#, IB_RMSE