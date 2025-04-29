import math

import Utility

location = {
    1: {"Id": "1", "location": "Hannoversche Str. 24, 31848 Bad Münder am Deister"},
    2: {"Id": "2", "location": "Osttangente 4, 31832 Springe"},
    3: {"Id": "3", "location": "Im Loffenkamp 2, 31832 Springe"},
    4: {"Id": "4", "location": "Wachlange 4, 31832 Springe"},
    5: {"Id": "5", "location": "Angerstraße 5, 31832 Springe"},
}

destination = {
    1: {"Id": "1", "destination": "Hannoversche Str. 24, 31848 Bad Münder am Deister"},
    2: {"Id": "2", "destination": "Osttangente 4, 31832 Springe"},
    3: {"Id": "3", "destination": "Im Loffenkamp 2, 31832 Springe"},
    4: {"Id": "4", "destination": "Wachlange 4, 31832 Springe"},
    5: {"Id": "5", "destination": "Angerstraße 5, 31832 Springe"},
}

taxi = {
    1: {"Id": "1", "location": "Lange Str. 60, 31832 Springe", "status": "driving", "battery": "60"},
    2: {"Id": "2", "location": "Calenberger Str. 17, 31832 Springe", "status":"available", "battery": "90"},
    3: {"Id": "3", "location": "An den Pappeln 2, 31832 Springe", "status": "charging", "battery": "78"},
    4: {"Id": "4", "location": "Spielburg 33, 31832 Springe", "status": "available", "battery": "20"},
    5: {"Id": "5", "location": "Am Kalkwerk 2a, 31832 Springe", "status": "available", "battery": "71"},
}

charger = {
    1: {"Id": "1", "name":"Tesla Supercharger", "location": "Lange Str. 1, 31832 Springe"},
    2: {"Id": "2", "name":"EnBW Charging Station", "location": "Osttangente 9, 31832 Springe"},
    3: {"Id": "3", "name":"GreenVesting Charging Station", "location": "Im Loffenkamp 2, 31832 Springe"},
    4: {"Id": "4", "name":"EnBW Charging Station", "location": "Eldagsener Str. 15, 31832 Springe"},
    5: {"Id": "5", "name":"Comfortcharge Charging Station", "location": "Im Stiege 9, 31832 Springe"},
}

def get_location_list():
    location_values = [f'{info["Id"]} {info["location"]}' for info in location.values()]
    return location_values

def get_destination_list():
    destination_values = [f'{info["Id"]} {info["destination"]}' for info in destination.values()]
    return destination_values

def get_taxi_list():
    taxi_values = [f'id:{info["Id"]}  location: {info["location"]}  status: {info["status"]}  battery: {info["battery"]}' for info in taxi.values()]
    return taxi_values

def get_charger_list():
    charger_values = [f'{info["Id"]}  location: {info["location"]}' for info in charger.values()]
    return charger_values

#  get the color based on taxi status
def get_taxi_font_color(taxi_id):
    status = taxi[taxi_id]["status"]
    if status == "available":
        return "green"
    elif status == "driving":
        return "red"
    elif status == "charging":
        return "yellow"
    return "black"

def update_taxi_status(taxi_id, status):
    taxi[taxi_id]["status"] = status

def update_taxi_battery_status(total_distance_km, taxi_id, new_location):
    charging_message = ""
    old_battery_status = int(taxi[taxi_id]["battery"])
    energy_consumption = 0.16     # 16,7 - 15,3 kWh/100 km according to VW [1] => mean 16  kWh/100 km => 0.16 per km
    battery_capacity = 59         # kWh e.g. ID3 pro according to VW
    battery_percentage_per_km = round((energy_consumption / battery_capacity) * 100, 2) # answer 0.27% for each km e.g. 10km need 2.7%
    needed_percentage = math.ceil(total_distance_km * battery_percentage_per_km)
    new_battery_status = old_battery_status - int(needed_percentage)
    # under 20% should go to charger cause the car will be available under 20% e.g. 16% and it wont be selected for another customer and wont go tp charger
    if new_battery_status <= 20:
      selected_charger_id = Utility.find_nearst_charger(new_location)
      charger_location = charger[int(selected_charger_id)]['location']
      charging_message = f"car is heading to charger with Id: {selected_charger_id} in {charger_location}"
      taxi[taxi_id]["status"] = "charging"
      taxi[taxi_id]["battery"] = new_battery_status  # set the new battery status
      taxi[taxi_id]["location"] = charger_location
    else:
      taxi[taxi_id]["battery"] = new_battery_status
      taxi[taxi_id]["status"] = "available"
      taxi[taxi_id]["location"] = new_location

    return charging_message
