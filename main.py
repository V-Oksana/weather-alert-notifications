import os
import requests
from twilio.rest import Client

# Openweather authorization
openweather_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
openweather_api_key = os.environ.get("openweather_api_key")

# Twilio authorization
auth_token = os.environ.get("AUTH_TOKEN")
account_sid = os.environ.get("ACCOUNT_SID")

# https://www.latlong.net - find latitude and longitude
weather_params = {
    "appid": openweather_api_key,
    # "lon": -119.698189,
    # "lat": 34.420830,
    "lon": -0.127758,
    "lat": 51.507351,
    "cnt": 4,
}

# Get weather forecast for next 12 hours
response = requests.get(openweather_endpoint, params=weather_params)
response.raise_for_status()
twelve_hour_forecast_data = response.json()

# Check if it's going to rain in the next 12 hours
bring_umbrella = False

for i in twelve_hour_forecast_data["list"]:
    # Codes below 700 in openweather database mean high chance of rain
    if i["weather"][0]["id"] < 700:
        bring_umbrella = True

# If high chance of rain in next 12 hours, send SMS alert to my phone number
if bring_umbrella:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Oksana, it's going to rain today. Don't forget your umbrella!",
        from_="whatsapp:+14155238886",
        to="whatsapp:+17739361340",
    )
    print(message.status)
