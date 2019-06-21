import json
import requests
import os

# ENDPOINT = "http://127.0.0.1:8000/api/dev-test/owners/"
#
#
# def do(method='get', data={}, is_json=True):
#     headers = {}
#     if is_json:
#         headers['content-type'] = 'application/json'
#         data = json.dumps(data)
#     r = requests.request(method, ENDPOINT, data=data, headers=headers)
#     print(r.text)
#     print(r.status_code)
#     return r
#
# do()


AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/"
# REFRESH_ENDPOINT = AUTH_ENDPOINT + "refresh/"

image_path = os.path.join(os.getcwd(), "ed.jpg")

headers = {
    "Content-Type": "application/json",
}

data = {
    'username': 'admin',
    'password': 'ggwp0077',
}

r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token = r.json()['token']
# print(token)


BASE_ENDPOINT = 'http://127.0.0.1:8000/api/owners/ed/cats/'

ENDPOINT = BASE_ENDPOINT + "admin_cat_3/"


headers2 = {
    # "Content-Type": "application/json",
    "Authorization": "JWT " + token
}

data2 = {
    'name': 'taffy',
    'breed': 'asian'
}

# Retrieve
# Delete

with open(image_path, 'rb') as image:
    file_data = {
        'image': image
    }
    # Retrieve
    r = requests.get(BASE_ENDPOINT, headers=headers2, files=file_data)
    print(r.text)

    # Update
    # r = requests.put(ENDPOINT, data=data2, headers=headers2, files=file_data)
    # print(r.text)

    # Create
    # r = requests.post(BASE_ENDPOInT, data=data2, headers=headers2, files=file_data)
    # print(r.text)
