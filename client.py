import requests
import json

URL = "http://localhost:5000/map-recommend"
response = requests.get(URL, data=json.dumps({"user": [{"latitude_0": 1, "longitude_0": 2},
                                                       {"latitude_1": 3, "longitude_1": 4},
                                                       {"latitude_2": 5, "longitude_2": 6}]}))
success = response.json()["success"]
print(response.json())

URL = 'http://localhost:5000/user-recommend'
user_id = 381
response = requests.get(URL, data=json.dumps({"user_id": user_id}))
print(response.json())

URL = 'http://localhost:5000/location-recommend'
location_id = 5315
response = requests.get(URL, data=json.dumps({"location_id": location_id}))
print(response.json())
