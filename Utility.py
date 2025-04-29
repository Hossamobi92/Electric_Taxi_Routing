import math
import TaxiDb
import requests

# global vars
total_distance_km = 0
total_duration_min = 0


def find_taxi(customer_location, customer_destination):
    #**1** select the available taxis
    available_taxis = get_available_taxis()

    #**2** measure distance between customer location and distination
    api_response = get_distance(customer_location, customer_destination)
    loc_to_dis_km = int(api_response['distance'])
    loc_to_dis_min = int(api_response['duration'])
    selected_taxi_id = None
    #**3** measure distance between customer and taxi location
    if available_taxis:
        shortest_distance = float('inf')  # the shortest drive way to the customer
        for taxi_id, info in available_taxis.items():
            #find a taxi in 10km range from customer location
            api_response = get_distance(info['location'], customer_location)
            distance = int(api_response['distance'])
            if distance <= 10:
                selected_taxi_battery = int(info['battery'])
                global total_distance_km
                total_distance_km = int(loc_to_dis_km + distance)  # kms between taxi location => customer location => customer destination
                enough_to_serve = check_battery_range(total_distance_km, selected_taxi_battery)
                if enough_to_serve: #check if taxi battery has enough percentage to service the customer
                    if distance < shortest_distance:
                        shortest_distance = distance
                        taxi_to_customer_min = int(api_response['duration'])
                        global total_duration_min
                        total_duration_min = loc_to_dis_min + taxi_to_customer_min  # minutes between taxi location => customer location => customer destination
                        selected_taxi_id = info['Id']
            else:
                selected_taxi_id = None
        return selected_taxi_id


def get_available_taxis():
    available_taxis = {taxi_id: info for taxi_id, info in TaxiDb.taxi.items() if info['status'] == 'available'}
    return available_taxis

def check_battery_range(total_distance_km, battery_status):
    enough_percentage = True
    energy_consumption = 0.16     # 16,7 - 15,3 kWh/100 km according to VW [1] => mean 16  kWh/100 km => 0.16 per km
    battery_capacity = 59         # kWh e.g. ID3 pro according to VW
    battery_percentage_per_km = round((energy_consumption / battery_capacity) * 100, 2) # answer 0.27% for each km e.g. 10km need 2.7%
    needed_percentage = math.ceil(total_distance_km * battery_percentage_per_km)
    rest = battery_status - needed_percentage
    if rest <= 15:  # should be enough to drive 40 km to find a charger
        enough_percentage = False
    return enough_percentage

def get_distance(origin, destination):
    url = "hier muss ein Google API Key hinzufügen"
    params = {
        'origins': origin,
        'destinations': destination,
        'key': "AIzaSyBhyDwu3Z8s9OarF1DJ9IzJS-IDMmE_zRU"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        elements = data['rows'][0]['elements'][0]
        if elements['status'] == 'OK':
            distance_meters = elements['distance']['value']
            duration_seconds = elements['duration']['value']
            distance_km = round(distance_meters / 1000.0)  # Convert to kilometers and round to the nearest integer
            duration_min = round(duration_seconds / 60.0)  # Convert duration to minutes and round to the nearest integer
            return {'distance': distance_km, 'duration': duration_min}
        else:
            return {'distance': "No distance data available", 'duration': "No duration data available"}
    else:
        return {'distance': "API request error", 'duration': "API request error"}

def find_nearst_charger(taxi_location):
    shortest_distance = float('inf')
    selected_charger_id = ""
    for charger_id, info in TaxiDb.charger.items():
        api_response = get_distance(taxi_location, info['location'])
        distance = int(api_response['distance'])
        if distance < shortest_distance:
            shortest_distance = distance
            selected_charger_id = info['Id']
    return selected_charger_id
