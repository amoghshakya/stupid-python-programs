# Pollution Sensors Simulation

This script simulates pollution sensors in Kathmandu. It generates random
values for PM2.5, PM10, temperature, and humidity, and
sends this data to a specified API endpoint every _n_ seconds.

```python
{
    "pm25": float
    "pm10": float
    "temperature": float
    "humidity": float
    "ts": int
}
```

## Setup

To be fair, you'll only likely need to install `python-dotenv` and `requests`.

```sh
pip install -r requirements.txt
```

Create a `.env` file in the same directory as the script with the following content:

```env
THINGSBOARD_ACCESS_TOKEN=<your_access_token>
```

Replace `<your_access_token>` with the actual access token for your ThingsBoard
device.
