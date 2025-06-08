import streamlit as st
import math

st.set_page_config(page_title="GeoLab Pro", layout="wide")
st.title("🧪 GeoLab Pro – University Geology Toolkit")

tool = st.sidebar.selectbox("Choose a Tool:", [
    "True Dip Calculator",
    "Grain Size to Phi",
    "Porosity Calculator",
    "Stratigraphic Thickness Estimator",
    "Coordinate Converter (Lat ↔ UTM)"
])

# 1️⃣ True Dip
if tool == "True Dip Calculator":
    st.header("📐 True Dip from Apparent Dip")
    ad = st.number_input("Apparent Dip (°)", 0.0)
    angle = st.number_input("Angle between directions (°)", 0.0, 90.0)
    if st.button("Calculate True Dip"):
        try:
            td = math.degrees(math.atan(math.tan(math.radians(ad)) / math.sin(math.radians(angle))))
            st.success(f"True Dip = {td:.2f}°")
        except:
            st.error("Error in calculation")

# 2️⃣ Grain Size ↔ Phi
elif tool == "Grain Size to Phi":
    st.header("🔁 Grain Size to Phi Scale")
    size = st.number_input("Grain Size (mm)", min_value=0.001)
    if st.button("Convert to Phi"):
        phi = -math.log2(size)
        st.success(f"φ = {phi:.2f}")

# 3️⃣ Porosity Calculator
elif tool == "Porosity Calculator":
    st.header("💧 Porosity from Volume")
    volume_pores = st.number_input("Pore Volume (cm³)")
    volume_total = st.number_input("Total Volume (cm³)")
    if volume_total > 0 and st.button("Calculate Porosity"):
        porosity = (volume_pores / volume_total) * 100
        st.success(f"Porosity = {porosity:.2f}%")

# 4️⃣ Stratigraphic Thickness
elif tool == "Stratigraphic Thickness Estimator":
    st.header("📏 Estimate True Thickness of a Bed")
    observed_thickness = st.number_input("Measured Thickness (m)")
    dip_angle = st.number_input("Dip Angle (°)", 0.0, 90.0)
    if st.button("Calculate True Thickness"):
        true_thickness = observed_thickness * math.sin(math.radians(dip_angle))
        st.success(f"True Thickness = {true_thickness:.2f} m")

# 5️⃣ Lat/Lon ↔ UTM (Simple Mock)
elif tool == "Coordinate Converter (Lat ↔ UTM)":
    st.header("🌐 Coordinate Converter (Basic)")
    lat = st.number_input("Latitude")
    lon = st.number_input("Longitude")
    if st.button("Mock Convert to UTM"):
        zone = int((lon + 180) / 6) + 1
        easting = (lon + 180) * 500
        northing = (lat + 90) * 1000
        st.info(f"UTM Zone: {zone}")
        st.success(f"Easting: {easting:.1f}, Northing: {northing:.1f} (Mock Values)")
