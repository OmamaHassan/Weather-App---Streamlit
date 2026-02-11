import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import datetime
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="🌦️ Weather Dashboard", layout = "wide")

# ----------------------------
# Helper: Weather background & animations
# ----------------------------
def weather_background(weather_main=None, is_day=True):
    # Default gradient (blue theme)
    sky = "#45B6E3"
    ground = "#ADD8E6"
    text_color = "#000000"
    anim_color = "#555555"

    if weather_main:
        if not is_day:
            sky = "#020111"
            ground = "#000000"
            text_color = "#ffffff"
            anim_color = "#ffffff"

    effects = ""


    # Clouds: show if cloudy or partly cloudy
    if weather_main in ["Clouds", "Clear"]:
        if is_day or weather_main == "Clouds":
            effects += """
            <div class="cloud x1"></div>
            <div class="cloud x2"></div>
            <div class="cloud x3"></div>
            <div class="sun"></div> 
            """
            
  
    # Stars: only at night
    if not is_day:
        effects += "".join("<div class='star'></div>" for _ in range(60))
        # Optional: moon
        effects += """
        <div class="moon"></div>
        """

    # Rain
    if weather_main == "Rain":
        effects += "".join("<div class='rain'></div>" for _ in range(120))

    # Snow
    if weather_main == "Snow":
        effects += "".join("<div class='snow'></div>" for _ in range(80))

    # Inject CSS + HTML

    st.markdown(f"""
    <style>
                
    html, body {{
        margin: 0;
        padding: 0;
        height: 100%;
        background: linear-gradient({sky}, {ground});
        color: {text_color};
    }}

    .stAppViewContainer {{
        background: linear-gradient({sky}, {ground});
        min-height: 100vh;
    }}

    .stApp {{
        background: transparent;
    }}

    header {{
        background: transparent !important;
    }}

    .stApp p, .stApp h1, .stApp h2, .stApp h3 {{
        color: {text_color} !important;
        text-shadow: 0 0 3px rgba(0,0,0,0.3);
    }}


    /* Rain */
    .rain {{
        position:fixed;width:2px;height:15px;background:{anim_color};
        animation:rain 0.7s linear infinite;left:calc(100%*var(--i));top:-20px;z-index:5;
    }}
    @keyframes rain {{to{{transform:translateY(110vh);}}}}

    /* Snow */
    .snow {{
        position:fixed;width:6px;height:6px;background:{anim_color};
        border-radius:50%;animation:snow 7s linear infinite;
        left:calc(100%*var(--i));top:-10px;z-index:5;
    }}
    @keyframes snow {{to{{transform:translateY(110vh) translateX(40px);}}}}

    .cloud{{
            position:fixed;
            width:260px;
            height:80px;
            background:linear-gradient(to bottom,#ffffff,#dfefff);
            border-radius:100px;
            opacity:0.85;
            filter: blur(1px);
            z-index:4;
    }}

    .cloud::before, .cloud::after{{
        content:'';
        position:absolute;
        background:inherit;
        width:140px;
        height:140px;
        top:-70px;
        left:30px;
        border-radius:50%;
    }}

    .cloud::after{{
        width:180px;
        height:180px;
        top:-90px;
        left:100px;
    }}

    .x1{{ top:12%; animation:moveclouds 90s linear infinite; }}
    .x2{{ top:28%; animation:moveclouds 120s linear infinite; transform:scale(0.8);}}
    .x3{{ top:44%; animation:moveclouds 180s linear infinite; transform:scale(1.1);}}

    @keyframes moveclouds{{
        from{{ left:-300px; }}
        to{{ left:100%; }}
    }}

    /* Stars */
    .star {{
        position:fixed;width:2px;height:2px;background:white;border-radius:50%;
        opacity:0.8;animation:starfall linear infinite;left:calc(100%*var(--i));top:-5px;z-index:3;
    }}
    @keyframes starfall{{to{{transform:translateY(100vh);}}}}

    /* Moon */
    .moon {{
        position:fixed;top:10%;right:10%;width:80px;height:80px;
        background:#fdfcdc;border-radius:50%;box-shadow:0 0 30px #fff;z-index:3;
    }}
    
    /* Sun */
    .sun {{
        position:fixed;
        top:10%;
        right:10%;
        width:80px;
        height:80px;
        background: #FFD700;  /* gold yellow */
        border-radius:50%;
        box-shadow: 0 0 40px #FFD700;
        z-index:3;
    }}

    
    .stMetric{{
        background:rgba(127, 0, 255, 0.5);
        padding:10px;
        border-radius:12px;
        backdrop-filter: blur(6px);
    }}

    </style>

    <div class="effects">{effects}</div>

    <script>
    document.querySelectorAll('.rain, .snow, .star').forEach(el => {{
        el.style.setProperty('--i', Math.random());
    }});
    </script>
    """, unsafe_allow_html=True)


# Apply default background (blue) first
weather_background()


# ----------------------------
# App content
# ----------------------------
st.title("🌦️ Weather Dashboard", text_alignment="center")
_, col, _ = st.columns([1, 2, 1])
with col:
    city = st.text_input("Enter city name")

if city.strip():
    # ----------------------------
    # Fetch location
    # ----------------------------
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_resp = requests.get(geo_url).json()
    if not geo_resp:
        st.error("City not found")
        st.stop()

    lat, lon = geo_resp[0]["lat"], geo_resp[0]["lon"]

    # ----------------------------
    # Fetch current weather
    # ----------------------------
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    weather = requests.get(weather_url).json()
    if weather.get("cod") != 200:
        st.error("Weather API error")
        st.stop()
   
    # Day/night determination
    current_time = weather["dt"]
    sunrise = weather["sys"]["sunrise"]
    sunset = weather["sys"]["sunset"]
    is_day = sunrise < current_time < sunset

    weather_main = weather["weather"][0]["main"]

    # Apply weather-based animations
    weather_background(weather_main, is_day)

    # ----------------------------
    # Current weather metrics (side by side)
    # ----------------------------


    # Convert UNIX timestamp to local time (you can also convert to city's local timezone if needed)
    last_updated = datetime.fromtimestamp(weather["dt"]).strftime("%I:%M %p")

    
    st.subheader(f"🌤 Weather in {city.title()} (Last updated: {last_updated})")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡 Temperature", f"{weather['main']['temp']} °C")
    with col2:
        st.metric("💧 Humidity", f"{weather['main']['humidity']}%")
    with col3:
        st.metric("☁ Condition", weather['weather'][0]['description'].title())


    # ----------------------------
    # Forecast
    # ----------------------------
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    forecast = requests.get(forecast_url).json()
    if forecast.get("cod") != "200":
        st.error("Forecast API error")
        st.stop()


    # Prepare 5-day forecast (midday for each day)
    forecast_list = forecast['list']
    daily_forecast = {}
    for entry in forecast_list:
        dt = pd.to_datetime(entry['dt_txt'])
        if dt.hour == 12:
            date_str = dt.date()
            daily_forecast[date_str] = {
                "temp_min": entry["main"]["temp_min"],
                "temp_max": entry["main"]["temp_max"],
                "humidity": entry["main"]["humidity"],
                "condition": entry["weather"][0]["description"].title(),
                "icon": entry["weather"][0]["icon"],
                "main": entry["weather"][0]["main"]
            }
        
    df = pd.DataFrame(forecast["list"])
    
    df["date"] = pd.to_datetime(df["dt_txt"])
    df["temp"] = df["main"].apply(lambda x: x["temp"])
    df['humidity'] = df['main'].apply(lambda x: x['humidity'])
    

    # Safely extract rain and snow from forecast['list']
    df['rain'] = df.apply(lambda row: row.get('rain', {}).get('3h', 0) if isinstance(row.get('rain', {}), dict) else 0, axis=1)
    df['snow'] = df.apply(lambda row: row.get('snow', {}).get('3h', 0) if isinstance(row.get('snow', {}), dict) else 0, axis=1)
    
    # Create total precipitation column
    df['precipitation'] = df['rain'] + df['snow']
    
    # Make sure 'weather_main' exists
    df['weather_main'] = df['weather'].apply(lambda x: x[0]['main'] if isinstance(x, list) and len(x) > 0 else 'Unknown')
    
    # Count occurrences of each weather type
    weather_counts = df['weather_main'].value_counts().reset_index()
    weather_counts.columns = ['weather', 'count']
    
    # Extract day and hour from datetime
    df['day'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour

    # Extract max/min temperatures safely
    df['temp_max'] = df['main'].apply(lambda x: x.get('temp_max', x['temp']))
    df['temp_min'] = df['main'].apply(lambda x: x.get('temp_min', x['temp']))


    st.subheader("⏱ Hourly Forecast")
    hourly_df = df[df['date'] <= df['date'].min() + pd.Timedelta(hours=24)]
    
    hourly_df["time"] = hourly_df["date"].dt.strftime("%I %p")
    hourly_df.iloc[0, hourly_df.columns.get_loc("time")] = "Now"

    hourly_cols = st.columns(len(hourly_df))

    for col, row in zip(hourly_cols, hourly_df.itertuples()):
        with col:
            st.markdown(f"""
            <div style="
                background: rgba(50, 50, 70, 0.4); /* semi-transparent card */
                backdrop-filter: blur(6px);
                border-radius: 12px;
                padding: 8px;
                text-align: center;
                min-width: 60px;
            ">
                <div style="font-size:12px; color:#fff;">{row.time}</div>
                <img src="https://openweathermap.org/img/wn/{row.weather[0]['icon']}.png" width="40">
                <div style="font-weight:bold; font-size:14px; color:#fff;">{round(row.temp)}°C</div>
            </div>
            <br>
            """, unsafe_allow_html=True)


    fig_hourly_temp = px.line(
            hourly_df,
            x="date",
            y="temp",
            markers=True,
            title="🌡 Hourly Temperature (°C)",
            color_discrete_sequence=["#ec7932"]
        )
    st.plotly_chart(fig_hourly_temp, use_container_width=True)


    col1, col2, col3 = st.columns(3)
    with col1:
        fig_hourly_humidity = px.line(
            hourly_df,
            x="date",
            y="humidity",
            markers=True,
            title="💧 Hourly Humidity (%)",
            labels={"humidity": "Humidity (%)", "date": "Time"},
        )

        st.plotly_chart(fig_hourly_humidity, use_container_width=True)
        
    with col2:
        fig_hourly_precipitation = px.bar(
            hourly_df,
            x="date",
            y="precipitation",
            title="💧 Hourly Precipitation (mm)"
        )
        st.plotly_chart(fig_hourly_precipitation, use_container_width=True)


    with col3:
        # Pivot to create 2D array: rows = day, columns = hour
        temp_matrix = df.pivot(index='day', columns='hour', values='temp')

        # Plot heatmap
        fig_heatmap = px.imshow(temp_matrix, labels=dict(x="Hour", y="Day", color="Temp °C"),  color_continuous_scale='Reds', title="🌡 Hourly Temperature Heatmap", aspect="auto")
        st.plotly_chart(fig_heatmap, use_container_width=True)



    st.subheader("🌤 5-Day Forecast")

    cols = st.columns(5)

    for i, (date, info) in enumerate(daily_forecast.items()):
        if i >= 5:
            break

        with cols[i]:
            day_name = date.strftime("%a")
            
            # Change card color based on day/night
            if is_day:
                bg_color =  "#4371C0"
                text_color = "#000000"
            else:
                bg_color = "#2B1047" 
                text_color = "#ffffff"

            st.markdown(f"""
            <div style="
                background-color:{bg_color};
                border-radius:15px;
                padding:10px;
                text-align:center;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
                color: {text_color};
            ">
                <h4 style="margin:5px">{day_name}</h4>
                <img src="http://openweathermap.org/img/wn/{info['icon']}@2x.png" width="80"/>
                <p style="margin:5px">🌡 {info['temp_min']}°C / {info['temp_max']}°C</p>
                <p style="margin:5px">💧 {info['humidity']}%</p>
                <p style="margin:5px">☁ {info['condition']}</p>
            </div>
            <br>
            """, unsafe_allow_html=True)
    
    

   
   

    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df, x="date", y="temp", markers=True, title = '📈 Temperature Forecast', labels={"temp":"Temp (°C)","date":"Date"}, color_discrete_sequence=["#ee7c18"])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig_humidity = px.line(df, x='date', y='humidity', markers=True, title = "💧 Humidity Forecast (%)", labels={"humidity":"Humidity (%)","date":"Date"})
        st.plotly_chart(fig_humidity, use_container_width=True)
     

    col1, col2 = st.columns(2)
    with col1:
        fig_precip = px.bar(df, x='date', y='precipitation', title = '💧 Precipitation Forecast (mm)', labels={"precipitation":"Precipitation(mm)", "date":"Date"}, color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig_precip, use_container_width=True)

    with col2:
        df['wind_speed'] = df['wind'].apply(lambda x: x.get('speed', 0))
        fig_wind = px.line(df, x='date', y='wind_speed', title = '🌬️ Wind Speed (m/s)', labels={"wind_speed":"Wind Speed (m/s)", "date":"Date"},color_discrete_sequence=['#2ecc71'])
        st.plotly_chart(fig_wind, use_container_width=True)
     

    col1, col2 = st.columns([1, 2])
    with col1:
        # Pie chart
        fig_weather = px.pie(weather_counts, names='weather', values='count', title='☁ Weather Type Distribution', color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig_weather, use_container_width=True)

    with col2: 
        fig_range = px.line(df, x='date', y='temp_max', title='🌡 Temperature Range', color_discrete_sequence=['#e74c3c'])

        # Fill between max and min temperatures
        fig_range.add_scatter(x=df['date'], y=df['temp_min'],
            fill='tonexty',      # fill down to previous y (temp_max)
            mode='none',
            fillcolor='rgba(231, 76, 60, 0.2)'
        )
        st.plotly_chart(fig_range, use_container_width=True)

