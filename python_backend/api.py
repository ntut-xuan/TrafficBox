import requests
import json
from flask import *

app = Flask(__name__)

bus_data_by_name = {}

@app.route("/nearbystation", methods=["GET"])
def NearByStation():

    lat = float(request.args.get("lat"))
    lng = float(request.args.get("lng"))
    radius = int(request.args.get("radius"))

    key = open("../gcp_secret", "r").read()

    bus_station_data = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?&language=zh-TW&location=%f,%f&radius=%d&types=bus_station&key=%s" % (lat, lng, radius, key))
    subway_station_data = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?&language=zh-TW&location=%f,%f&radius=%d&types=subway_station&key=%s" % (lat, lng, radius, key))

    bus_station_set = set()
    result = {}

    bus_station_json_object = json.loads(bus_station_data.text)

    for object in bus_station_json_object["results"]:
        name = object["name"]
        bus_station_set.add(name)

    for name in bus_station_set:
        if name not in bus_data_by_name:
            continue
        if name not in result:
            result[name] = []
        for stationID in bus_data_by_name[name].keys():
            stops = []
            for stop in bus_data_by_name[name][stationID]["stops"]:
                stops.append(stop["RouteName"]["Zh_tw"])
            result[name].append({"stationID": stationID, "lat": bus_data_by_name[name][stationID]["lat"], "lng": bus_data_by_name[name][stationID]["lng"], "stops": stops})

    return result
    

bus_stop_api_data = open("./static/bus_stop.json", "r", encoding="utf8").read()
bus_station_api_data = open("./static/bus_station.json", "r", encoding="utf8").read()

bus_stop_api_jsonObject = json.loads(bus_stop_api_data)
bus_station_api_jsonObject = json.loads(bus_station_api_data)


if __name__ == "__main__":

    for bus_station in bus_station_api_jsonObject:
        if bus_station["StationName"]["Zh_tw"] not in bus_data_by_name:
            bus_data_by_name[bus_station["StationName"]["Zh_tw"]] = {}
        bus_data_by_name[bus_station["StationName"]["Zh_tw"]][bus_station["StationID"]] = {"name":  bus_station["StationName"]["Zh_tw"], "lat": bus_station["StationPosition"]["PositionLat"], "lng": bus_station["StationPosition"]["PositionLon"], "stops": bus_station["Stops"]}


    app.debug = True
    app.run(host="0.0.0.0", port=80)

#print(NearByStation(25.0021392, 121.5572114, 1000))