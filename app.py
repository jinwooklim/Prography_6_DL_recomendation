from flask import Flask, request, Response, jsonify
from http import HTTPStatus
from model import SiameseNetwork
import json
import torch

device = "cuda:0"

app = Flask(__name__)

model = SiameseNetwork().to(device)
model.load_state_dict(torch.load("./model2.pt", map_location=torch.device(device)))
model.eval()

A = 1


@app.route("/a")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/b', methods=['POST'])
def map_recomend():
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
    # print("A", A.to("cpu").tolist())
    d_128 = vector.to("cpu").tolist()

    return jsonify({'success': True,
                    'vector': d_128
                    }), HTTPStatus.OK


# start flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
