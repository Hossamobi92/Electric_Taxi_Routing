import threading
import time
import TaxiDb


def run_periodically(interval, func):
    while True:
        func()
        time.sleep(interval)


def start_periodic_task():
    thread = threading.Thread(target=run_periodically, args=(180, update_taxi_battery))
    thread.daemon = True  # This makes sure the thread will not prevent the program from exiting
    thread.start()

def update_taxi_battery():
    charging_taxis = {key: value for key, value in TaxiDb.taxi.items() if value["status"] == "charging"}
    if charging_taxis:
        for key, value in charging_taxis.items():
            taxi_id = int(value['Id'])
            old_soc = int(value['battery'])
            if old_soc < 100:
                new_soc = charge_taxi_battery(old_soc)
                TaxiDb.taxi[taxi_id]["battery"] = str(new_soc)
                if new_soc >= 80:
                    TaxiDb.taxi[taxi_id]["status"] = "available"


def charge_taxi_battery(soc):
    soc_t0 = soc / 100               # Convert SOC from percentage to decimal
    battery_capacity = 59            # Battery capacity in kWh
    power_consumption = 10           # Constant power consumption in kW
    time_interval_hours = 180 / 3600  # Convert seconds to hours
    energy_consumed = power_consumption * time_interval_hours  # Calculate energy consumed during the time interval in kWh
    delta_soc = energy_consumed / battery_capacity  # Calculate change in SOC
    soc_t = soc_t0 + delta_soc  # Calculate new SOC at time t

    return round(soc_t * 100)


