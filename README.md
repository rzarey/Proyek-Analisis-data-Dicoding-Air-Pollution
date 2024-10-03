# Air Quality Analysis Dashboard: Beijing

[![Screenshot of Dashboard](link-ke-screenshot.png)](https://github.com/rzarey/Proyek-Analisis-data-Dicoding-Air-Pollution.git)

## Project Overview

This interactive dashboard analyzes air quality data from 12 stations in Beijing, China, covering the period from 2013 to 2017. The goal is to explore trends in major air pollutants (PM2.5, PM10, SO2, NO2, CO, O3) and understand air quality variations across different cities in Beijing. 

The dashboard provides insights into:

- Yearly trends for individual pollutants in each city.
- City-specific comparisons of pollutant levels for a selected year. 
- Seasonal variations in pollution levels.
- Correlations between different pollutants.
- The relationship between rainfall and pollutant levels.

This project was created as part of a Dicoding final project in collaboration with Bangkit Academy. It serves as a practical example of data analysis and visualization techniques using Python libraries like Pandas, Matplotlib, Plotly, and Streamlit. 

## How to Run the Dashboard

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/rzarey/Proyek-Analisis-data-Dicoding-Air-Pollution.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd Proyek-Analisis-data-Dicoding-Air-Pollution
   ```

3. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv .venv 
   ```

4. **Activate the Virtual Environment:**
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

5. **Install Required Libraries:**
   ```bash
   pip install -r requirements.txt 
   ```

6. **Run the Streamlit App:**
   ```bash
   streamlit run dashboard.py
   ```

The dashboard will open in your web browser. 

## Data

The dataset used in this project contains hourly air quality measurements from 12 stations in Beijing. You can find the data files in the `data` directory. 

## Author

- **Name:** Reyhanssan islamey
- **Email:** m179b4ky3775@bangkit.academy
- **Dicoding Profile:** [https://www.dicoding.com/users/imalivejustin/academies](https://www.dicoding.com/users/imalivejustin/academies)

## Demo

You can try a live demo of the dashboard here: [https://github.com/rzarey/Proyek-Analisis-data-Dicoding-Air-Pollution.git](https://beijingairpollution.streamlit.app)
