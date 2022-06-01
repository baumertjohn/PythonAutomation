# 100 Days of Code Capstone Project
# Python Automation
# A simple app to send overnight temps for the next 5 days as SMS.
# Run via PythonAnywhere or similar or self-hosted.

import os
import smtplib

import requests
from dotenv import load_dotenv

load_dotenv()

# The following variables are stored in an .env for privacy
MY_EMAIL = os.getenv("MY_EMAIL")  # Gmail account to send message from
PASSWORD = os.getenv("PASSWORD")  # Password for Gmail account
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")  # Gmail SMTP address
PHONE = os.getenv("PHONE")  # Phone number "email" for SMS message
GEONAME_USER = os.getenv("GEONAME_USER")  # Geonames.org username
HOME_LOCATION = os.getenv("HOME_LOCATION")  # Format as "XXX/##,##"


def send_sms_message(location, weather_message):
    message = f"\n{location} Overnight Forecast\n{weather_message[:-1]}"
    with smtplib.SMTP(SMTP_ADDRESS, 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL, to_addrs=PHONE, msg=message.encode("utf-8")
        )


def get_lat_lon(weather_data):
    lat0 = weather_data["geometry"]["coordinates"][0][0][1]
    lon0 = weather_data["geometry"]["coordinates"][0][0][0]
    lat2 = weather_data["geometry"]["coordinates"][0][2][1]
    lon2 = weather_data["geometry"]["coordinates"][0][2][0]
    new_lat = (lat0 + lat2) / 2
    new_lon = (lon0 + lon2) / 2
    return new_lat, new_lon


def get_city(latitude, longitude):
    location_params = {
        "lat": latitude,
        "lng": longitude,
        "username": GEONAME_USER,
    }

    location_resp = requests.get(
        "http://api.geonames.org/findNearbyJSON", params=location_params
    )
    location_resp.raise_for_status()
    location_data = location_resp.json()
    return location_data["geonames"][0]["name"]


def main():
    try:
        response = requests.get(
            f"https://api.weather.gov/gridpoints/{HOME_LOCATION}/forecast"
        )
        response.raise_for_status()
        weather_data = response.json()
        weather_list = [value for value in weather_data["properties"]["periods"]]
        weather_message = ""

        for index in range(len(weather_list)):
            if not weather_list[index]["isDaytime"]:
                if weather_list[index]["temperature"] <= 39:
                    warning = " ❄❄❄"
                else:
                    warning = ""
                weather_message += (
                    f"{weather_list[index]['name']}: "
                    f"{weather_list[index]['temperature']}{warning}\n"
                )

    except requests.HTTPError as exception:
        weather_message = exception

    lat, lon = get_lat_lon(weather_data)
    city = get_city(lat, lon)
    send_sms_message(city, weather_message)


if __name__ == "__main__":
    main()
