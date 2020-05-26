from flask import Flask, request, Response, jsonify
from http import HTTPStatus
from model import SiameseNetwork
import json
import torch

from utils import cosine_similarity
import numpy as np
import pandas as pd

# Setting for PyTorch
device = "cpu"
model = SiameseNetwork().to(device)
model.load_state_dict(torch.load("./data/model2.pt", map_location=torch.device(device)))
model.eval()

# Setting for Flask
app = Flask(__name__)

# Get User, Location entity is not implemented.
# So We use, a csv file for this API.
header = ['user_id', 'location_id', 'frequency']
user_location_table = pd.read_csv('./data/preprocessed_data2.csv', sep='\t', names=header)
n_users = user_location_table.user_id.unique().shape[0]
n_locations = user_location_table.location_id.unique().shape[0]
user_location_table = user_location_table.to_numpy()
user_location_frequency_matrix = np.zeros((n_users, n_locations))
# User x Location matrix
# user_location_frequency_matrix can be replaced to user-match-location table JOIN.
for checkin in user_location_table:
    user_location_frequency_matrix[checkin[0], checkin[1]] = checkin[2]


@app.route('/map-recommend', methods=['GET'])
def map_recommend():
    request_data = json.loads(request.data)["user"]

    latitude_0 = request_data[0]["latitude_0"]
    longitude_0 = request_data[0]["longitude_0"]
    latitude_1 = request_data[1]["latitude_1"]
    longitude_1 = request_data[1]["longitude_1"]
    latitude_2 = request_data[2]["latitude_2"]
    longitude_2 = request_data[2]["longitude_2"]

    latitude_0 = torch.Tensor([latitude_0]).type(torch.FloatTensor).unsqueeze(dim=0).to(device)
    longitude_0 = torch.Tensor([longitude_0]).type(torch.FloatTensor).unsqueeze(dim=0).to(device)
    latitude_1 = torch.Tensor([latitude_1]).type(torch.FloatTensor).unsqueeze(dim=0).to(device)
    longitude_1 = torch.Tensor([longitude_1]).type(torch.FloatTensor).unsqueeze(dim=0).to(device)
    latitude_2 = torch.Tensor([latitude_2]).type(torch.FloatTensor).unsqueeze(dim=0).to(device)
    longitude_2 = torch.Tensor([longitude_2]).type(torch.FloatTensor).unsqueeze(dim=0).to(device)

    vector_tensor = model(latitude_0, longitude_0, latitude_1, longitude_1, latitude_2, longitude_2)
    vector = vector_tensor.to("cpu").squeeze(dim=0)
    d_128 = vector.to("cpu").tolist()

    return jsonify({'success': True,
                    'vector': d_128
                    }), HTTPStatus.OK


@app.route("/user-recommend", methods=['GET'])
def get_memory_based_user_recommendation():
    request_data = json.loads(request.data)["user_id"]

    # User x User matrix
    user_similarity = cosine_similarity(user_location_frequency_matrix, kind='user')
    selected_user_similarity = user_similarity[request_data]

    # return top-10 similarity user's id
    # Ref : https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array
    top10_id = selected_user_similarity.argsort()[-11:][::-1]  # cost : O(N)
    top10_id = top10_id[1:11]  # remove it self
    top10_sim = selected_user_similarity[top10_id]
    top10 = {'user_ids': top10_id.tolist(),
             'user_sims': top10_sim.tolist()}
    return jsonify({'success': True,
                    'top10': top10
                    }), HTTPStatus.OK


@app.route("/location-recommend", methods=['GET'])
def get_memory_based_location_recommendation():
    request_data = json.loads(request.data)["location_id"]

    # Location x Location matrix
    location_similarity = cosine_similarity(user_location_frequency_matrix, kind='location')
    selected_location_similarity = location_similarity[request_data]

    # return top-10 similarity location's id
    # Ref : https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array
    top10_id = selected_location_similarity.argsort()[-11:][::-1]  # cost : O(N)
    top10_id = top10_id[1:11]  # remove it self
    top10_sim = selected_location_similarity[top10_id]
    top10 = {'location_ids': top10_id.tolist(),
             'location_sims': top10_sim.tolist()}
    return jsonify({'success': True,
                    'top10': top10
                    }), HTTPStatus.OK


# start flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
