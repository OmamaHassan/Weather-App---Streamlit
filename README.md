# 🌦️ Weather Dashboard

An interactive weather dashboard built with **Streamlit** that shows current weather, hourly forecasts, and 5-day forecasts for cities using the **OpenWeatherMap API**. Includes animated backgrounds and visualizations for temperature, humidity, precipitation, wind, and weather conditions.

## Features

-  Search any city and view current weather  
-  Hourly forecast with temperature, humidity, and precipitation  
-  5-day forecast
-  Animated weather backgrounds (clouds, sun, moon)  
-  Interactive charts using **Plotly**  
-  Responsive layout with Streamlit columns


## Tech Stack

- Python  
- Streamlit  
- Pandas  
- Plotly Express  
- OpenWeatherMap API  
- dotenv for environment variables


## Project Structure

```
Weather-Dashboard/
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── .env # Store your OpenWeatherMap API key
└── README.md
```

## Setup & Usage

1. Clone the repository
2. Install dependencies
3. Create a .env file
4. Add your OpenWeatherMap API key to .env
5. streamlit run app.py

## Visualizations

* Line charts for temperature, humidity, etc.
* Bar charts for precipitation
* Heatmap for temperature variation
* Pie chart for weather condition distribution


## Data Source

Weather data is fetched using the OpenWeatherMap API.


## Weather Dashboard Demo

### Demo1
![=Weather Dashboard Demo 1](Demo/Night.gif)

### Demo2
![Weather Dashboard Demo 2](Demo/Day.gif)
