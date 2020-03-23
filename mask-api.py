import requests as re
from haversine import haversine
json_data = re.get('https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/stores/json').json()

store_infos = json_data['storeInfos']

my_location = (37.505360, 126.901104) # latitude, longitude

distance_limit_km = 3

for store_info in store_infos:
    store_location = (store_info['lat'],store_info['lng'])

    distance_in_km = haversine(my_location, store_location)

    if distance_in_km < distance_limit_km:
        print({"상호명": store_info["name"], "주소":store_info["addr"], "거리" : f"{distance_in_km:.2f}km"})