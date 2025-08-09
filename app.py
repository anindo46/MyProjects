import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import io
from streamlit_lottie import st_lottie
import requests

# --------- PAGE CONFIG -----------
st.set_page_config(
    page_title="GeoLab Pro | By Anindo Paul Sourav",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🧪"
)

# --------- LOAD LOTTIE -----------
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --------- FOOTER FUNCTION -----------
def footer():
    st.markdown("""
        <style>
            footer {
                visibility: visible;
                text-align: center;
                padding: 10px 0px;
                color: #888888;
                font-size: 12px;
                margin-top: 3rem;
            }
        </style>
        <footer>
            Developed with ❤️ by <b>Anindo Paul Sourav</b> — University of Barishal
        </footer>
        """, unsafe_allow_html=True)

# --------- SIDEBAR -----------
with st.sidebar:
    st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=120)
    st.markdown("### GeoLab Pro")
    st.caption("Smart Geoscience Toolkit")
    st.markdown("---")

# --------- MODULE LIST -----------
MODULES = {
    "📊 MIA Tool": "mia_tool",
    "🧭 Stereonet Plotter": "stereonet_plotter",
    "🧭 True Dip Calculator": "true_dip_calculator",
    "🪨 Porosity Calculator": "porosity_calculator",
    "📏 Stratigraphic Thickness Estimator": "stratigraphic_thickness_estimator",
    "⛰️ Slope Gradient (%)": "slope_gradient",
    "🌾 Grain Size to Phi": "grain_size_to_phi"
}

# --------- HELPER: SHOW & DOWNLOAD PLOT -----------
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

# --------- TOOL UIs -----------
def mia_tool():
    st.subheader("📊 MIA Tool")
    st.info("🚧 This module is coming soon! Stay tuned.")

def stereonet_plotter():
    st.subheader("🧭 Stereonet Plotter")
    
    strike_plane = st.number_input("Strike of Plane (°)", 0.0, 360.0, step=1.0)
    dip_plane = st.number_input("Dip of Plane (°)", 0.0, 90.0, step=1.0)
    trend_line = st.number_input("Trend of Line (°)", 0.0, 360.0, step=1.0)
    plunge_line = st.number_input("Plunge of Line (°)", 0.0, 90.0, step=1.0)
    
    calculate = st.button("🔍 Plot Stereonet")
    
    if calculate:
        strike_plane_rad = math.radians(strike_plane)
        dip_plane_rad = math.radians(dip_plane)
        trend_line_rad = math.radians(trend_line)
        plunge_line_rad = math.radians(plunge_line)
        
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(111, projection='polar')
        
        ax.plot([strike_plane_rad, strike_plane_rad + math.pi], [dip_plane_rad, dip_plane_rad], label='Plane', color='b')
        ax.plot([trend_line_rad, trend_line_rad + math.pi], [plunge_line_rad, plunge_line_rad], label='Line', color='r')
        
        ax.set_title("Stereonet Plot")
        ax.legend()
        
        show_and_download(fig, "stereonet_plot.png")

def true_dip_calculator():
    st.subheader("🧭 True Dip from Apparent Dip")
    ad = st.number_input("Apparent Dip (°)", 0.0, step=0.1)
    angle = st.number_input("Angle Between Directions (°)", 0.0, 90.0, step=0.1)
    calculate = st.button("🔍 Calculate True Dip")
    if calculate:
        if angle == 0:
            st.error("Angle between directions must be > 0°")
            return
        td = math.degrees(math.atan(math.tan(math.radians(ad)) / math.sin(math.radians(angle))))
        st.success(f"✅ True Dip = {td:.2f}°")
        st.markdown(r"**Formula:** True Dip = tan⁻¹(tan(Apparent Dip) / sin(Angle))")

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        b, h = 1, np.tan(np.radians(ad))
        x, y = [0, b, b], [0, 0, h]
        ax.plot(x + [0], y + [0], 'k-', lw=2)
        ax.fill(x + [0], y + [0], 'lavender', alpha=0.5)
        ax.text(0.5, -0.1, f"Angle = {angle}°", ha='center')
        ax.text(b+0.1, h/2, f"Apparent = {ad}°", va='center')
        ax.text(b/2, h+0.1, f"True Dip = {td:.2f}°", ha='center', fontweight='bold')
        ax.axis('off')
        show_and_download(fig, "true_dip_diagram.png")

def porosity_calculator():
    st.subheader("🪨 Porosity % from Volume")
    pores = st.number_input("Pore Volume (cm³)", 0.0, step=0.1)
    total = st.number_input("Total Volume (cm³)", 0.0, step=0.1)
    calculate = st.button("🔍 Calculate Porosity")
    if total > 0 and calculate:
        porosity = (pores / total) * 100
        solid = total - pores
        st.success(f"✅ Porosity = {porosity:.2f}%")
        st.markdown(r"**Formula:** Porosity = (Pore Volume / Total Volume) × 100")

        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.barh(["Rock"], [pores], color='skyblue', label="Pores")
        ax.barh(["Rock"], [solid], left=[pores], color='saddlebrown', label="Solids")
        ax.set_xlim(0, total)
        ax.legend(loc="lower right")
        ax.set_title("Pore vs Solid Distribution")
        ax.set_facecolor('#f4f4f4')
        ax.get_yaxis().set_visible(False)
        show_and_download(fig, "porosity_diagram.png")

def stratigraphic_thickness_estimator():
    st.subheader("📏 Stratigraphic Thickness Estimation")
    measured = st.number_input("Measured Thickness (m)", 0.0, step=0.1)
    dip = st.number_input("Dip Angle (°)", 0.0, 90.0, step=0.1)
    calculate = st.button("🔍 Calculate True Thickness")
    if dip > 0 and calculate:
        true_thick = measured * math.sin(math.radians(dip))
        st.success(f"✅ True Thickness = {true_thick:.2f} m")
        st.markdown(r"**Formula:** T = Measured × sin(Dip)")

        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, measured], 'saddlebrown', lw=3, label='Measured')
        ax.plot([0, 1], [0, true_thick], 'limegreen', lw=3, label='True')
        ax.legend()
        ax.set_title("Measured vs. True Thickness")
        ax.set_ylabel("Thickness (m)")
        show_and_download(fig, "stratigraphy_diagram.png")

def slope_gradient():
    st.subheader("⛰️ Slope Gradient (%)")
    rise = st.number_input("Vertical Rise (m)", 0.0, step=0.1)
    run = st.number_input("Horizontal Run (m)", 0.0, step=0.1)
    calculate = st.button("🔍 Calculate Slope Gradient")
    if run > 0 and calculate:
        slope = (rise / run) * 100
        st.success(f"✅ Slope Gradient = {slope:.2f}%")
        st.markdown(r"**Formula:** Slope % = (Rise / Run) × 100")

        fig, ax = plt.subplots()
        ax.plot([0, run], [0, 0], 'k--')
        ax.plot([0, run], [0, rise], 'b-', lw=2)
        ax.fill([0, run, run], [0, 0, rise], color='skyblue', alpha=0.3)
        ax.text(run/2, rise/2, f"{slope:.1f}%", fontsize=10, ha='center')
        ax.set_xlim(0, run+1)
        ax.set_ylim(0, rise+1)
        ax.set_title("Slope Profile")
        ax.axis('off')
        show_and_download(fig, "slope_diagram.png")

def grain_size_to_phi():
    st.subheader("🌾 Grain Size to Phi (φ)")
    size = st.number_input("Grain Size (mm)", 0.0, step=0.01)
    calculate = st.button("🔍 Calculate Phi")
    if size > 0 and calculate:
        phi = -math.log2(size)
        st.success(f"✅ φ = {phi:.2f}")
        st.markdown(r"**Formula:** φ = –log₂(Grain Size in mm)")

        fig, ax = plt.subplots()
        ax.plot([size], [phi], marker='o', markersize=10, color='crimson')
        ax.set_xlabel("Grain Size (mm)")
        ax.set_ylabel("Phi (φ)")
        ax.set_title("Grain Size → φ Scale")
        ax.grid(True)
        show_and_download(fig, "phi_diagram.png")

# --------- HOMEPAGE WITH MODULE SELECTOR -----------

def display_home():
    st.markdown(
        """
        <style>
        .main-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 70vh;
            gap: 3rem;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .left-section {
            flex: 1;
            max-width: 350px;
        }
        .right-section {
            flex: 1;
            max-width: 500px;
        }
        h1 {
            color: #1F77B4;
            font-weight: 700;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        p.lead {
            font-size: 1.25rem;
            color: #333333;
            margin-bottom: 1.5rem;
            line-height: 1.5;
        }
        .select-container {
            margin-top: 2rem;
        }
        .stSelectbox > div {
            background-color: #f0f4f8;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 1.1rem;
            font-weight: 600;
            color: #0B3954;
        }
        </style>
        """, unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        lottie_json = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")
        if lottie_json:
            st_lottie(lottie_json, speed=1, loop=True, height=350)
        else:
            st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=300)
    with col2:
        st.markdown("<h1>Welcome to GeoLab Pro</h1>", unsafe_allow_html=True)
        st.markdown('<p class="lead">A comprehensive and professional geoscience toolkit, crafted for students and researchers.<br> Choose your desired module below to begin.</p>', unsafe_allow_html=True)
        selected_module = st.selectbox("📦 Select a Module to Start", list(MODULES.keys()), index=0, key="module_select_home")
        return selected_module

# --------- MAIN -----------
def main():
    st.title("")  # clear default top title for clean look

    selected_module = display_home()

    st.markdown("---")

    # Call the right tool based on selection
    if selected_module:
        if MODULES[selected_module] == "mia_tool":
            mia_tool()
        elif MODULES[selected_module] == "stereonet_plotter":
            stereonet_plotter()
        elif MODULES[selected_module] == "true_dip_calculator":
            true_dip_calculator()
        elif MODULES[selected_module] == "porosity_calculator":
            porosity_calculator()
        elif MODULES[selected_module] == "stratigraphic_thickness_estimator":
            stratigraphic_thickness_estimator()
        elif MODULES[selected_module] == "slope_gradient":
            slope_gradient()
        elif MODULES[selected_module] == "grain_size_to_phi":
            grain_size_to_phi()

    footer()

if __name__ == "__main__":
    main()
