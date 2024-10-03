import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
import os

# data_path = r"D:\Kuliah\Semester 5\BANGKIT\Dicoding Air Quality Analysis\data"
data_path = r"data"

def load_data(file_name):
    df = pd.read_csv(os.path.join(data_path, file_name))
    df['city'] = file_name.split('_')[2].split('.')[0]
    return df

data_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
all_data = pd.concat([load_data(file) for file in data_files], ignore_index=True)

for col in ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']:
    all_data[col] = pd.to_numeric(all_data[col], errors='coerce')
    all_data[col] = all_data[col].fillna(all_data[col].mean())

all_data['datetime'] = pd.to_datetime(all_data[['year', 'month', 'day', 'hour']])
all_data = all_data.drop(['year', 'month', 'day', 'hour', 'No'], axis=1)

pollutant_info = {
    'PM2.5': {
        'description': "Particulate matter less than 2.5 micrometers in diameter. These fine particles can penetrate deep into the lungs and bloodstream, causing respiratory and cardiovascular problems.",
        'health_effects': "Respiratory illnesses, cardiovascular disease, lung cancer, premature death."
    },
    'PM10': {
        'description': "Particulate matter less than 10 micrometers in diameter. While larger than PM2.5, PM10 can still irritate the respiratory system.",
        'health_effects': "Respiratory irritation, coughing, asthma, reduced lung function."
    },
    'SO2': {
        'description': "Sulfur dioxide is a gas produced from burning fossil fuels. It contributes to acid rain and can cause respiratory problems.",
        'health_effects': "Respiratory irritation, breathing difficulties, asthma, lung damage."
    },
    'NO2': {
        'description': "Nitrogen dioxide is a gas produced from vehicle exhaust and industrial emissions. It can damage the respiratory system and contribute to smog.",
        'health_effects': "Respiratory problems, airway inflammation, increased susceptibility to infections, cardiovascular effects."
    },
    'CO': {
        'description': "Carbon monoxide is a colorless, odorless gas produced from incomplete combustion. It is poisonous and can reduce the oxygen-carrying capacity of blood.",
        'health_effects': "Headaches, dizziness, nausea, confusion, heart problems, death (at high concentrations)."
    },
    'O3': {
        'description': "Ozone is a gas that can be beneficial in the upper atmosphere but harmful at ground level. Ground-level ozone is formed from reactions involving pollutants from vehicles and industry.",
        'health_effects': "Respiratory problems, chest pain, coughing, throat irritation, reduced lung function, asthma."
    }
}

st.set_page_config(page_title="Air Quality Analysis - Beijing", page_icon=":cityscape:")
st.markdown("""
    <style>
    .main {
        background-color: #282c34;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #1f2126;
    }
    .stButton>button {
        background-color: #61dafb;
        color: #282c34;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1f2126;
        color: #ffffff;
        text-align: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="navbar">
        <span style="font-size: 24px; font-weight: bold;">Air Quality Analysis - Beijing</span>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.header("Filter Data")
year = st.sidebar.slider('Select Year', min_value=2013, max_value=2017, value=2017)

selected_data = st.selectbox("Select Data to Display", [
    'Pollutant Trends for a City',
    'Compare Cities for a Pollutant',
    'Yearly Pollutant Comparison',
    'Daily Pollutant Levels',
    'Correlation Heatmap',
    'Seasonal Trend Analysis',
    'Pollutant Distribution',
    'Time Series Decomposition',
    'Rainfall vs. Pollutant Levels'
])

if selected_data in ['Pollutant Trends for a City', 'Daily Pollutant Levels', 'Time Series Decomposition', 'Rainfall vs. Pollutant Levels']:
    city = st.sidebar.selectbox('Select City', all_data['city'].unique())

if selected_data in ['Pollutant Trends for a City', 'Compare Cities for a Pollutant', 'Yearly Pollutant Comparison',
                     'Daily Pollutant Levels', 'Seasonal Trend Analysis', 'Pollutant Distribution', 'Time Series Decomposition', 'Rainfall vs. Pollutant Levels']:
    pollutant = st.sidebar.selectbox('Select Pollutant', list(pollutant_info.keys()))

if selected_data == 'Compare Cities for a Pollutant':
    selected_cities = st.sidebar.multiselect('Select Cities to Compare', all_data['city'].unique(), default=all_data['city'].unique()[:2])

filtered_data = all_data[(all_data['datetime'].dt.year == year)]
if selected_data in ['Pollutant Trends for a City', 'Daily Pollutant Levels', 'Time Series Decomposition', 'Rainfall vs. Pollutant Levels']:
    filtered_data = filtered_data[filtered_data['city'] == city]
if selected_data == 'Compare Cities for a Pollutant':
    filtered_data = filtered_data[filtered_data['city'].isin(selected_cities)]

if selected_data == 'Pollutant Trends for a City':
    st.header(f"{pollutant} Trends in {city}")
    st.markdown(f"**About {pollutant}:**")
    st.write(pollutant_info[pollutant]['description'])
    st.write(f"**Health Effects:** {pollutant_info[pollutant]['health_effects']}")
    fig = px.line(all_data[all_data['city'] == city], x='datetime', y=pollutant,
                  title=f'{pollutant} Trends in {city}',
                  color_discrete_sequence=['lightskyblue'])
    st.plotly_chart(fig)

    yearly_avg = filtered_data.groupby(filtered_data['datetime'].dt.year)[pollutant].mean()
    st.write(f"""
    **Insight and Analysis for {city}:**
    The average {pollutant} concentration in {city} for {year} was {yearly_avg.get(year, 'N/A'):.2f}. 
    """)

elif selected_data == 'Compare Cities for a Pollutant':
    st.header(f"Comparison of {pollutant} Levels in Selected Cities")
    st.markdown(f"**About {pollutant}:**")
    st.write(pollutant_info[pollutant]['description'])
    st.write(f"**Health Effects:** {pollutant_info[pollutant]['health_effects']}")
    fig = px.line(filtered_data, x='datetime', y=pollutant, color='city',
                  title=f"{pollutant} Levels in Selected Cities",
                  color_discrete_sequence=px.colors.qualitative.Dark2)
    st.plotly_chart(fig)

    city_avg = filtered_data[filtered_data['datetime'].dt.year == year].groupby('city')[pollutant].mean().sort_values()
    highest_city = city_avg.index[-1]
    lowest_city = city_avg.index[0]
    st.write(f"""
    **Insight and Analysis for Selected Cities:**

    In {year}, {highest_city} had the highest average {pollutant} concentration ({city_avg[highest_city]:.2f}), 
    while {lowest_city} had the lowest ({city_avg[lowest_city]:.2f}).

    **Recommendation:** Based on {pollutant} levels alone, {lowest_city} might be a better place to live 
    in terms of air quality compared to the other selected cities in {year}. 
    However, it's essential to consider other factors and pollutants for a comprehensive assessment.
    """)

elif selected_data == 'Yearly Pollutant Comparison':
    st.header(f"Yearly {pollutant} Comparison Across Cities")
    st.markdown(f"**About {pollutant}:**")
    st.write(pollutant_info[pollutant]['description'])
    st.write(f"**Health Effects:** {pollutant_info[pollutant]['health_effects']}")
    yearly_city_data = all_data.groupby(['city', all_data['datetime'].dt.year])[pollutant].mean().reset_index()
    fig = px.bar(yearly_city_data, x='city', y=pollutant, color='city', animation_frame='datetime',
                 range_y=[0, yearly_city_data[pollutant].max() * 1.1],
                 title=f"Yearly {pollutant} Comparison Across Cities")
    st.plotly_chart(fig)

    yearly_city_avg = all_data[all_data['datetime'].dt.year == year].groupby('city')[pollutant].mean().sort_values()
    highest_city = yearly_city_avg.index[-1]
    lowest_city = yearly_city_avg.index[0]

    st.write(f"""
    **Insight and Analysis for {year}:**

    In {year}, {highest_city} had the highest average {pollutant} concentration ({yearly_city_avg[highest_city]:.2f}), 
    while {lowest_city} had the lowest ({yearly_city_avg[lowest_city]:.2f}).
    """)

elif selected_data == 'Daily Pollutant Levels':
    st.header(f"Daily {pollutant} Levels in {city} for {year}")
    st.markdown(f"**About {pollutant}:**")
    st.write(pollutant_info[pollutant]['description'])
    st.write(f"**Health Effects:** {pollutant_info[pollutant]['health_effects']}")

    daily_avg = filtered_data.groupby(filtered_data['datetime'].dt.date)[pollutant].mean().reset_index()
    daily_avg.columns = ['Date', pollutant]

    fig = px.line(daily_avg, x='Date', y=pollutant,
                  title=f'Daily {pollutant} Levels in {city} for {year}',
                  color_discrete_sequence=['lightskyblue'])
    st.plotly_chart(fig)

elif selected_data == 'Correlation Heatmap':
    st.header("Interactive Correlation Heatmap of Air Quality Indicators")
    selected_columns = st.multiselect('Select Columns for Correlation', filtered_data.columns, default=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'WSPM'])

    if selected_columns:
        corr = filtered_data[selected_columns].corr()
        fig = px.imshow(corr,
                        title=f"Correlation Heatmap for {year} (Selected Columns)",
                        color_continuous_scale='RdBu_r')
        st.plotly_chart(fig)

elif selected_data == 'Seasonal Trend Analysis':
    st.header(f"Seasonal Trend Analysis of {pollutant} in {year}")
    st.markdown(f"**About {pollutant}:**")
    st.write(pollutant_info[pollutant]['description'])
    st.write(f"**Health Effects:** {pollutant_info[pollutant]['health_effects']}")

    monthly_avg = filtered_data.groupby(filtered_data['datetime'].dt.month)[pollutant].mean()
    fig = px.line(x=monthly_avg.index, y=monthly_avg.values,
                  title=f"Average Monthly {pollutant} Levels in {year}",
                  labels={'x': 'Month', 'y': f'Average {pollutant}'})
    st.plotly_chart(fig)


elif selected_data == 'Pollutant Distribution':
    st.header(f"{pollutant} Distribution in {year}")
    st.markdown(f"**About {pollutant}:**")
    st.write(pollutant_info[pollutant]['description'])
    st.write(f"**Health Effects:** {pollutant_info[pollutant]['health_effects']}")

    fig = px.box(filtered_data, x='city', y=pollutant,
                 title=f"{pollutant} Distribution Across Cities in {year}",
                 color='city', color_discrete_sequence=px.colors.qualitative.Dark2)
    st.plotly_chart(fig)


elif selected_data == 'Time Series Decomposition':
    st.header(f"Time Series Decomposition of {pollutant} in {city} (2013-2017)")
    st.markdown(f"**About {pollutant}:**")
    st.write(pollutant_info[pollutant]['description'])
    st.write(f"**Health Effects:** {pollutant_info[pollutant]['health_effects']}")

    try:
        city_data = all_data[all_data['city'] == city]
        daily_data = city_data.set_index('datetime').resample('D')[pollutant].mean()
        decomposed = seasonal_decompose(daily_data, model='additive', period=365)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=decomposed.trend.index, y=decomposed.trend, mode='lines', name='Trend'))
        fig.add_trace(go.Scatter(x=decomposed.seasonal.index, y=decomposed.seasonal, mode='lines', name='Seasonality'))
        fig.add_trace(go.Scatter(x=decomposed.resid.index, y=decomposed.resid, mode='lines', name='Residuals'))

        fig.update_layout(title=f"Time Series Decomposition of {pollutant} in {city} (2013-2017)",
                          xaxis_title="Date", yaxis_title=f"{pollutant} Concentration")
        st.plotly_chart(fig)

    except ValueError as e:
        st.error(f"Unable to perform time series decomposition: {e}")

elif selected_data == 'Rainfall vs. Pollutant Levels':
    st.header(f"Rainfall vs. {pollutant} Levels in {city} for {year}")
    st.markdown(f"**About {pollutant}:**")
    st.write(pollutant_info[pollutant]['description'])
    st.write(f"**Health Effects:** {pollutant_info[pollutant]['health_effects']}")

    fig = px.scatter(filtered_data, x='RAIN', y=pollutant, trendline='ols',
                     title=f'Rainfall vs. {pollutant} Levels in {city} for {year}',
                     labels={'RAIN':'Rainfall (mm)', 'y':f'{pollutant} Concentration'})
    st.plotly_chart(fig)

if st.checkbox("Show Data"):
    st.subheader("Filtered Data")
    st.write(filtered_data)

st.markdown("""
    <div class="footer">
        Created by Reyhanssan islamey | m179b4ky3775@bangkit.academy | <a href="https://www.dicoding.com/users/imalivejustin/academies" target="_blank">Dicoding Profile</a>
    </div>
    """, unsafe_allow_html=True)
