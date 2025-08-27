import requests
import pandas as pd
from simplekml import Kml

# Lista miast WRM razem z ID :
# 148 - Wrocław
# 891 - Kobierzyce
# 892 - Wisznia
# 893 - Kąty Wrocławskie
# 1176 - Siechnice
# 1177 - Czernica

city_ids = [148, 1176, 1177, 891, 893, 892]

all_stations = []

for city_id in city_ids:
    url = f"https://api.nextbike.net/maps/nextbike-live.json?city={city_id}"
    data = requests.get(url).json()

    # Lista stacji
    places = data["countries"][0]["cities"][0]["places"]

    for p in places:
        area = p["name"].split(" - ")[0]
        all_stations.append({
            "area": area,
            "station_name": p["name"],
            "lat": p["lat"],
            "lng": p["lng"],
            "bike_racks": p.get("bike_racks", None)
        })

df = pd.DataFrame(all_stations)

# Zapis do CSV
df.to_csv("wrm_stations_all.csv", index=False)

# Zapis do KML
kml = Kml()
for _, row in df.iterrows():
    kml.newpoint(name=row["station_name"], coords=[(row["lng"], row["lat"])])
kml.save("wrm_stations_all.kml")

print("Zapisano wszystkie stacje do wrm_stations_all.csv i wrm_stations_all.kml")
