import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import io
from streamlit_lottie import st_lottie
import requests

from qfl_mia_tool import qfl_and_mia_tool  # Your custom tool

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(
    page_title="GeoLab Pro",
    layout="wide",
    page_icon="🌍"
)

MODULES = {
    "QFL & MIA Tool": "qfl_mia_tool",
    "Stereonet Plotter": "stereonet_plotter",
    "True Dip Calculator": "true_dip_calculator",
    "Porosity Calculator": "porosity_calculator",
    "Stratigraphic Thickness Estimator": "strat_thickness_estimator",
    "Slope Gradient (%)": "slope_gradient",
    "Grain Size to Phi": "grain_size_to_phi"
}

def show_and_download(fig, filename="diagram.png"):
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.download_button(
        label="📥 Download Diagram as PNG",
        data=buf.getvalue(),
        file_name=filename,
        mime="image/png"
    )

# Your modules' UIs (same as before) ...
def qfl_mia_tool_ui():
    st.header("QFL & MIA Tool")
    qfl_and_mia_tool()

def stereonet_plotter():
    st.header("🧭 Stereonet Plotter")
    strike_plane = st.number_input("Strike of Plane (°)", 0.0, 360.0)
    dip_plane = st.number_input("Dip of Plane (°)", 0.0, 90.0)
    trend_line = st.number_input("Trend of Line (°)", 0.0, 360.0)
    plunge_line = st.number_input("Plunge of Line (°)", 0.0, 90.0)
    if st.button("🔍 Plot Stereonet"):
        strike_rad = math.radians(strike_plane)
        dip_rad = math.radians(dip_plane)
        trend_rad = math.radians(trend_line)
        plunge_rad = math.radians(plunge_line)

        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(111, projection='polar')
        ax.plot([strike_rad, strike_rad + math.pi], [dip_rad, dip_rad], label='Plane', color='b')
        ax.plot([trend_rad, trend_rad + math.pi], [plunge_rad, plunge_rad], label='Line', color='r')
        ax.set_title("Stereonet Plot")
        ax.legend()
        show_and_download(fig, "stereonet_plot.png")

def true_dip_calculator():
    st.header("🧭 True Dip from Apparent Dip")
    ad = st.number_input("Apparent Dip (°)", 0.0)
    angle = st.number_input("Angle Between Directions (°)", 0.0, 90.0)
    if st.button("🔍 Calculate"):
        if angle == 0:
            st.error("Angle must be > 0")
        else:
            td = math.degrees(math.atan(math.tan(math.radians(ad)) / math.sin(math.radians(angle))))
            st.success(f"✅ True Dip = {td:.2f}°")
            st.markdown(r"**Formula:** True Dip = tan⁻¹(tan(Apparent Dip) / sin(Angle))")

def porosity_calculator():
    st.header("🪨 Porosity % from Volume")
    pores = st.number_input("Pore Volume (cm³)", 0.0)
    total = st.number_input("Total Volume (cm³)", 0.0)
    if st.button("🔍 Calculate"):
        if total == 0:
            st.error("Total Volume must be > 0")
        else:
            porosity = (pores / total) * 100
            st.success(f"✅ Porosity = {porosity:.2f}%")

def stratigraphic_thickness_estimator():
    st.header("📏 Stratigraphic Thickness Estimation")
    measured = st.number_input("Measured Thickness (m)", 0.0)
    dip = st.number_input("Dip Angle (°)", 0.0, 90.0)
    if st.button("🔍 Calculate"):
        true_thick = measured * math.sin(math.radians(dip))
        st.success(f"✅ True Thickness = {true_thick:.2f} m")

def slope_gradient():
    st.header("⛰️ Slope Gradient (%)")
    rise = st.number_input("Vertical Rise (m)", 0.0)
    run = st.number_input("Horizontal Run (m)", 0.0)
    if st.button("🔍 Calculate"):
        if run == 0:
            st.error("Horizontal Run must be > 0")
        else:
            slope = (rise / run) * 100
            st.success(f"✅ Slope Gradient = {slope:.2f}%")

def grain_size_to_phi():
    st.header("🌾 Grain Size to Phi (φ)")
    size = st.number_input("Grain Size (mm)", 0.0)
    if st.button("🔍 Calculate"):
        if size <= 0:
            st.error("Grain size must be > 0")
        else:
            phi = -math.log2(size)
            st.success(f"✅ φ = {phi:.2f}")

# --- New Homepage with animated Earth globe and student theme ---
def display_homepage():
    st.markdown("""
    <style>
    .home-title {
        font-size: 3rem;
        font-weight: 700;
        color: #0A74DA;
        margin-bottom: 0;
    }
    .home-subtitle {
        font-size: 1.25rem;
        margin-top: 0;
        color: #444444;
    }
    .feature-list {
        font-size: 1.1rem;
        margin-top: 1rem;
        list-style-type: none;
        padding-left: 0;
        color: #555555;
    }
    .feature-list li {
        margin-bottom: 0.5rem;
        padding-left: 25px;
        position: relative;
    }
    .feature-list li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #0A74DA;
        font-weight: bold;
    }
    .start-btn {
        margin-top: 2rem;
        font-size: 1.25rem;
        background-color: #0A74DA;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .start-btn:hover {
        background-color: #005bb5;
    }
    </style>
    """, unsafe_allow_html=True)

    lottie_earth = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_3ntisyuc.json")  # Animated Earth globe

    col1, col2 = st.columns([1, 2])
    with col1:
        if lottie_earth:
            st_lottie(lottie_earth, height=350, speed=1, loop=True)
        else:
            st.write("Animated Earth failed to load.")
    with col2:
        st.markdown('<h1 class="home-title">Welcome to GeoLab Pro</h1>', unsafe_allow_html=True)
        st.markdown('<p class="home-subtitle">A student-friendly, professional toolkit for Geoscience enthusiasts.</p>', unsafe_allow_html=True)
        st.markdown("""
        <ul class="feature-list">
            <li>Instant geological & geoscience calculations</li>
            <li>Easy-to-use interface for students & researchers</li>
            <li>Export results & visualizations</li>
        </ul>
        """, unsafe_allow_html=True)

        selected = st.selectbox("Or select a module here:", list(MODULES.keys()))
        if st.button("Start Exploring"):
            st.session_state.selected_module = MODULES[selected]
            st.experimental_rerun()

def sidebar_navigation():
    st.sidebar.title("Modules")
    current = st.session_state.selected_module
    selected_display = [k for k,v in MODULES.items() if v==current][0]
    selected = st.sidebar.selectbox("Switch Module", list(MODULES.keys()), index=list(MODULES.values()).index(current))
    if MODULES[selected] != current:
        st.session_state.selected_module = MODULES[selected]
        st.experimental_rerun()
    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 Back to Home"):
        st.session_state.selected_module = None
        st.experimental_rerun()

def main():
    if "selected_module" not in st.session_state:
        st.session_state.selected_module = None

    if st.session_state.selected_module is None:
        display_homepage()
    else:
        sidebar_navigation()
        mod = st.session_state.selected_module

        if mod == "qfl_mia_tool":
            qfl_mia_tool_ui()
        elif mod == "stereonet_plotter":
            stereonet_plotter()
        elif mod == "true_dip_calculator":
            true_dip_calculator()
        elif mod == "porosity_calculator":
            porosity_calculator()
        elif mod == "strat_thickness_estimator":
            stratigraphic_thickness_estimator()
        elif mod == "slope_gradient":
            slope_gradient()
        elif mod == "grain_size_to_phi":
            grain_size_to_phi()

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; font-size:12px; color:gray; padding:10px;">
        Developed by Anindo Paul Sourav — University of Barishal
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
