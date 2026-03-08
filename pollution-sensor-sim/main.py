import requests
import random
import time
import dotenv  # pip install python-dotenv
import logging
import os

from db import SensorBuffer

# create a .env file in the same directory with the following content:
# THINGSBOARD_ACCESS_TOKEN=your_device_access_token
env_exists = dotenv.load_dotenv()

if not env_exists:
    logging.fatal(
        ".env file not found. Please create a .env file with the following content:\nTHINGSBOARD_ACCESS_TOKEN=your_device_access_token"
    )
    exit(1)

access_token = os.getenv("THINGSBOARD_ACCESS_TOKEN")
API_URL = f"http://eu.thingsboard.cloud/api/v1/{access_token}/telemetry"

SEND_INTERVAL = 5  # seconds between telemetry

# initialize local db if not exists
db = SensorBuffer()
if not os.path.exists("sensor_buffer.db"):
    logging.info("Initialized local sensor buffer database")

# set initial sensor values instead of randomly assigning them
# we can then simulate changes over time more realistically
pm25 = random.uniform(30, 70)
pm10 = random.uniform(60, 140)
temperature = random.uniform(15, 25)
humidity = random.uniform(40, 70)
co2 = random.uniform(400, 800)
no2 = random.uniform(10, 50)


def generate_sensor_data():
    # global keyword basically allows us to modify above defined variables
    # normally you wouldn't be able to do this inside a function because
    # blocke scope
    global pm25, pm10, temperature, humidity, co2, no2

    # simulating gradual changes in sensor readings
    # this seems more realistic than generating completely random values each time
    pm25 += random.uniform(-5, 5)
    pm10 += random.uniform(-10, 10)
    temperature += random.uniform(-0.5, 0.5)
    humidity += random.uniform(-2, 2)
    co2 += random.uniform(-20, 20)
    no2 += random.uniform(-5, 5)

    # if it's too humid, we assume particulate matters settle down
    if humidity > 70:
        pm25 *= 0.95
        pm10 *= 0.95
        no2 *= 0.98  # NO2 also tends to decrease in high humidity

    # we can simulate a pollution spike randomly (small probability)
    if random.random() < 0.07:
        pm25 += random.randint(10, 25)
        pm10 += random.randint(20, 80)
        co2 += random.randint(50, 150)
        no2 += random.randint(10, 20)

    # spike bhayepachi decay garaudai lyaune
    PM25_BASELINE = 80
    PM10_BASELINE = 150
    CO2_BASELINE = 600
    NO2_BASELINE = 30
    DECAY_RATE = 0.05
    # baseline value tira ghataudai tara 5% difference each time
    # without 5%, siddhai baseline value tira janchha, not realistic
    pm25 += (PM25_BASELINE - pm25) * DECAY_RATE
    pm10 += (PM10_BASELINE - pm10) * DECAY_RATE
    co2 += (CO2_BASELINE - co2) * DECAY_RATE
    no2 += (NO2_BASELINE - no2) * DECAY_RATE

    # upper and lower bounds to keep values from going into unrealistic ranges
    pm25 = max(5, min(pm25, 180))
    pm10 = max(pm25 * 1.3, min(pm10, 250))  # prevent PM10 from being less than PM2.5
    temperature = max(5, min(temperature, 35))
    humidity = max(20, min(humidity, 90))

    return {
        "pm25": round(pm25, 2),
        "pm10": round(pm10, 2),
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "co2": round(co2, 2),
        "no2": round(no2, 2),
        "ts": int(time.time() * 1000),
    }


# send data to thingsboard api
def send_to_thingsboard(data):
    try:
        response = requests.post(API_URL, json=data, timeout=5)

        if response.status_code == 200:
            logging.info(f"[SENT] {data}")
            return True
        else:
            logging.error(
                f"[ERROR] Failed to send data: {response.status_code} - {response.text}"
            )
            return False

    except requests.exceptions.RequestException:
        logging.error("[ERROR] Connection failed")
        return False


# main loop here
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",  # time, log level, message
    )
    logging.info("IoT Air Quality Simulator started")

    while True:
        telemetry = generate_sensor_data()

        success = send_to_thingsboard(telemetry)

        # POST request gayena bhane database ma store garne
        if not success:
            logging.warning("[BUFFER] Storing data locally due to send failure")
            print("[BUFFER] Storing data locally")
            db.store_locally(telemetry)
        else:
            # arko choti POST req garda nagayeko data pathaune
            db.resend_buffered_data(API_URL)

        time.sleep(SEND_INTERVAL)
