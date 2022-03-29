import requests
print(requests.get("http://124.222.81.160:5000/datetime").json())
print(requests.get("http://124.222.81.160:5000/room?keyword=七海").json())
print(requests.get("http://124.222.81.160:5000/medalnames?roomid=80397").json())
print(requests.get("http://124.222.81.160:5000/medallevels?roomid=80397&medalid=80397").json())