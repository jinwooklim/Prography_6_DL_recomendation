import requests
import json
import os
from PIL import Image
import imghdr
import argparse

URL = "http://localhost:5000/b"
# alpha_user_id, alpha_sample0_latitude, alpha_sample0_longitude, alpha_sample1_latitude, alpha_sample1_longitude, alpha_sample2_latitude, alpha_sample2_longitude

response = requests.post(URL, data=json.dumps({"user": [{"latitude_0": 1, "longitude_0": 2},
                                                        {"latitude_1": 3, "longitude_1": 4},
                                                        {"latitude_2": 5, "longitude_2": 6}]}))
# [[위도0,경도0],[위도1,경도1],[위도2,경도2]]

success = response.json()["success"]

print(success)

print(response.json())
