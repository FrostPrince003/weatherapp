
import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get API key (local: from .env, cloud: from secrets)
API_KEY = os.getenv("WEATHERAPI_KEY") or st.secrets.get("WEATHERAPI_KEY")

# Sidebar for app title and input
st.sidebar.title("🌤 WeatherVista")

if not API_KEY:
    st.sidebar.error("API Key not found. Please set it in .env for local or as a secret for deployment.")
else:
    # Input city in the sidebar
    city = st.sidebar.text_input("Enter the city name:", key="city_input")

    # Main app layout
    st.markdown(
        """
        <style>
        .main {
            background-color: #1E1E1E;
            color: white;
        }
        .stSidebar {
            background-color: #282828;
            color: white;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #F0F0F0;
        }
        .reportview-container {
            background-color: #1E1E1E;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Welcome to WeatherVista 🌟")
    st.markdown(
        """
        Get real-time weather updates for any city in the world!
        
        *Tips:*
        - Use the sidebar to enter a city name.
        - Results will appear below if valid.
        """
    )

    if city:
        # WeatherAPI endpoint
        BASE_URL = "http://api.weatherapi.com/v1/current.json"

        # Make API request
        params = {"key": API_KEY, "q": city, "aqi": "no"}
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            # Extract weather data
            location = data["location"]["name"]
            region = data["location"]["region"]
            country = data["location"]["country"]
            temp_c = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            wind_kph = data["current"]["wind_kph"]
            humidity = data["current"]["humidity"]

            # Weather display layout
            st.header(f"Weather in {location}, {region}, {country}")
            st.markdown(
                f"""
                - *Condition:* {condition}
                - *Temperature:* {temp_c}°C
                - *Wind Speed:* {wind_kph} km/h
                - *Humidity:* {humidity}%
                """
            )
        else:
            st.error("City not found. Please try again.")