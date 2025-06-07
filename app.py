import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("🗺️ GeoSmart Tutor - Bangladesh")

location = st.text_input("Enter District or Upazila:")

if location:
    st.subheader("📄 Geological Summary")
    st.write(f"Geological summary for **{location}**:")
    st.markdown("- Formation: Dupi Tila (example)")
    st.markdown("- Age: Pleistocene")
    st.markdown("- Lithology: Clay, silt, sand")

    st.subheader("🪨 Rock / Mineral Types")
    st.markdown("- Quartz, Feldspar, Mica")
    st.markdown("- Sedimentary rocks")

    st.subheader("⚠️ Environmental Risks")
    st.markdown("- Flood Risk: High")
    st.markdown("- Erosion Risk: Medium")

    st.subheader("🛰 NDWI / Map")
    map_center = [23.6850, 90.3563]
    m = folium.Map(location=map_center, zoom_start=6)
    folium.Marker(map_center, popup=location).add_to(m)
    st_folium(m, width=700)

    if st.checkbox("বাংলায় দেখুন"):
        st.markdown("**ভূতাত্ত্বিক সারাংশ:**")
        st.markdown("- গঠন: দূপি তিলা")
        st.markdown("- খনিজ: কোয়ার্টজ, ফেল্ডস্পার")
        st.markdown("- বন্যার ঝুঁকি: উচ্চ")
else:
    st.info("🔍 Please enter a location to begin...")
