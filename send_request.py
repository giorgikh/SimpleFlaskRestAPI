import requests

BASE = "http://127.0.0.1:5000/"
# insert
data = [{"name": "video_name", "likes": 232, "views": 35900},
        {"name": "qwert", "likes": 211132, "views": 13213},
        {"name": "sadasd", "likes": 3213, "views": 5563},
        {"name": "asdad", "likes": 545, "views": 87654}]
for i in range(len(data)):
    response = requests.put(
        BASE + "video/" + str(i), data[i])
    print(response.json())

# update
response = requests.patch(BASE + "video/1", {})
print(response.json())
# get
response = requests.get(BASE + "video/1")
print(response.json())

# delete
response = requests.delete(BASE + "video/2")
print(response)
