# Pollution Sensors Simulation

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
