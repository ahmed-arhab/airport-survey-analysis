import streamlit as st
import csv
import matplotlib.pyplot as plt
import os

# --- 1. SETUP & DATA LOADING ---
st.set_page_config(page_title="Airport Analysis", layout="wide")

# This cache prevents reloading data on every click
@st.cache_data
def load_data(year, airport_code):
    filename = f"{airport_code}{year}.csv"
    
    # Smart path handling (fixes your FileNotFoundError)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)

    data_list = []
    if not os.path.exists(full_path):
        return None # Return None if file missing
        
    with open(full_path, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader) # Skip header
        for row in csvreader:
            data_list.append(row)
    return data_list

# --- 2. DICTIONARIES (Your original data) ---
air_port = {
    "LHR":"London Heathrow", "MAD":"Madrid Adolfo Suarez-Barajas",
    "CDG":"Charles De Gaulle", "IST":"Istanbul Airport",
    "AMS":"Amsterdam Schiphol", "LIS":"Lisbon Portela",
    "FRA":"Frankfurt Main", "FCO":"Rome Fiumicino",
    "MUC":"Munich International", "BCN":"Barcelona International"
}

code_of_air_lines = {
    "BA":"British Airways", "AF":"Air France", "AY":"Finnair",
    "KL":"KLM", "SK":"Scandinavian", "TP":"TAP Portugal",
    "TK":"Turkish Airlines", "U2":"easyJet", "FR":"Ryanair",
    "A3":"Aegean", "SN":"Brussels Airlines", "EK":"Emirates",
    "QR":"Qatar Airways", "IB":"Iberia", "LH":"Lufthansa"
}

# --- 3. WEBSITE UI ---
st.title("✈️ Airport Flight Analysis Dashboard")
st.markdown("Enter the details below to analyze flight patterns.")

# Sidebar for Inputs
with st.sidebar:
    st.header("Configuration")
    selected_code = st.selectbox("Select Airport", options=list(air_port.keys()), format_func=lambda x: f"{x} - {air_port[x]}")
    selected_year = st.text_input("Enter Year (YYYY)", "2017")
    
    run_button = st.button("Analyze Data")

# --- 4. MAIN LOGIC ---
if run_button:
    # Load the data
    data_list = load_data(selected_year, selected_code)
    
    if data_list is None:
        st.error(f"❌ Could not find file: {selected_code}{selected_year}.csv")
        st.info("Make sure the CSV file is in the same folder as this script.")
    else:
        st.success(f"✅ Loaded data for {air_port[selected_code]} ({selected_year})")
        
        # --- CALCULATIONS (Your Task B Logic) ---
        total_flights = len(data_list)
        
        term_2 = sum(1 for x in data_list if x[8] == "2")
        under_600 = sum(1 for x in data_list if int(x[5]) < 600)
        
        # Air France Count
        af_count = sum(1 for x in data_list if x[1].startswith("AF"))
        
        # Temp below 15
        temp_low = sum(1 for x in data_list if float(x[10].split('°')[0]) < 15)
        
        # BA Stats
        ba_count = sum(1 for x in data_list if x[1].startswith("BA"))
        ba_avg = round(ba_count/12, 2)
        ba_pct = round((ba_count/total_flights)*100, 2)
        
        # Rain Hours
        rainy_hours = set()
        for x in data_list:
            if "rain" in x[10].lower():
                rainy_hours.add(int(x[2].split(':')[0]))
        
        # Least Common Dest
        dest_counts = {}
        for x in data_list:
            dest = x[4]
            dest_counts[dest] = dest_counts.get(dest, 0) + 1
        least_dest_code = min(dest_counts, key=dest_counts.get)
        least_dest_name = air_port.get(least_dest_code, least_dest_code)

        # --- DISPLAY METRICS ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Flights", total_flights)
        col2.metric("Terminal 2 Departures", term_2)
        col3.metric("Flights < 600 miles", under_600)
        
        col4, col5, col6 = st.columns(3)
        col4.metric("Air France Flights", af_count)
        col5.metric("Avg BA Flights/Hr", ba_avg)
        col6.metric("Rainy Hours", len(rainy_hours))
        
        st.markdown("---")
        st.subheader(f"📉 Least Common Destination: **{least_dest_name}**")

        # --- HISTOGRAM SECTION (Your Task D Logic adapted for Web) ---
        st.markdown("### 📊 Airline Histogram")
        airline_input = st.selectbox("Select Airline for Histogram", options=list(code_of_air_lines.keys()), format_func=lambda x: f"{x} - {code_of_air_lines[x]}")
        
        if airline_input:
            # Prepare data for graph
            hour_counts = {h:0 for h in range(24)}
            for row in data_list:
                if airline_input in row[1]:
                    hour = int(row[2].split(':')[0])
                    hour_counts[hour] += 1
            
            # Filter to show only active hours (0-12 based on your logic)
            hours = list(range(13))
            counts = [hour_counts[h] for h in hours]
            
            # Create Plot using Matplotlib (Web compatible)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(hours, counts, color="#3498db", edgecolor="#2c3e50")
            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Number of Flights")
            ax.set_title(f"Departures for {code_of_air_lines[airline_input]}")
            ax.set_xticks(hours)
            
            # Show graph on website
            st.pyplot(fig)