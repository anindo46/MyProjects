import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import io
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="GeoLab Pro", layout="wide", page_icon="🧪")

# --- Sidebar ---
st.sidebar.title("🧪 GeoLab Pro")
st.sidebar.info("A Smart Geoscience Toolkit by Anindo Paul Sourav\n\nUniversity of Barishal")
st.sidebar.markdown("---")
st.sidebar.caption("🔍 Choose a tool from the selector below")

# --- Title and Credit ---
st.markdown("""
    <style>
        .title-bar { display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }
        .title-bar img { width: 50px; }
        .title-bar h2 { margin: 0; }
        .credit { font-size: 14px; color: gray; margin-top: -10px; }
    </style>
    <div class="title-bar">
        <img src="https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png">
        <div>
            <h2>GeoLab Pro</h2>
            <p class="credit">Developed by Anindo Paul Sourav – Student, Geology and Mining, University of Barishal</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Tool Selector ---
tool = st.selectbox("Choose a Tool / একটি টুল বেছে নিন:", [
    "True Dip Calculator",
    "Porosity Calculator",
    "Stratigraphic Thickness Estimator",
    "Slope Gradient (%)",
    "Grain Size to Phi",
    "Stereonet Plotter"
])

# --- Helper: Show and Download Matplotlib Figure ---
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

# --- Stereonet Plotter ---
if tool == "Stereonet Plotter":
    st.subheader("🧭 Stereonet Plotter")
    
    # Input Fields
    st.sidebar.markdown("### Stereonet Plotter Instructions")
    st.sidebar.markdown("""
    - **Strike & Dip**: Enter the strike (0-360°) and dip (0-90°) angles for a plane.
    - **Trend & Plunge**: Enter the trend (0-360°) and plunge (0-90°) for a line.
    - You can rotate and contour poles to visualize complex geological structures.
    """)
    
    strike_plane = st.number_input("Strike of Plane (°)", 0.0, 360.0)
    dip_plane = st.number_input("Dip of Plane (°)", 0.0, 90.0)
    trend_line = st.number_input("Trend of Line (°)", 0.0, 360.0)
    plunge_line = st.number_input("Plunge of Line (°)", 0.0, 90.0)
    
    calculate = st.button("🔍 Plot Stereonet")
    
    if calculate:
        # Convert input to radians for plotting
        strike_plane_rad = math.radians(strike_plane)
        dip_plane_rad = math.radians(dip_plane)
        trend_line_rad = math.radians(trend_line)
        plunge_line_rad = math.radians(plunge_line)
        
        # Plot the Stereonet
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(111, projection='polar')
        
        # Plot Plane
        ax.plot([strike_plane_rad, strike_plane_rad + math.pi], [dip_plane_rad, dip_plane_rad], label='Plane', color='b')
        
        # Plot Line
        ax.plot([trend_line_rad, trend_line_rad + math.pi], [plunge_line_rad, plunge_line_rad], label='Line', color='r')
        
        ax.set_title("Stereonet Plot")
        ax.legend()
        
        # Show and download plot
        show_and_download(fig, "stereonet_plot.png")

# --- True Dip Calculator ---
elif tool == "True Dip Calculator":
    st.subheader("🧭 True Dip from Apparent Dip")
    ad = st.number_input("Apparent Dip (°)", 0.0)
    angle = st.number_input("Angle Between Directions (°)", 0.0, 90.0)
    calculate = st.button("🔍 Calculate")
    if calculate:
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

# --- Porosity Calculator ---
elif tool == "Porosity Calculator":
    st.subheader("🪨 Porosity % from Volume")
    pores = st.number_input("Pore Volume (cm³)", 0.0)
    total = st.number_input("Total Volume (cm³)", 0.0)
    calculate = st.button("🔍 Calculate")
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

# --- Stratigraphic Thickness Estimator ---
elif tool == "Stratigraphic Thickness Estimator":
    st.subheader("📏 Stratigraphic Thickness Estimation")
    measured = st.number_input("Measured Thickness (m)", 0.0)
    dip = st.number_input("Dip Angle (°)", 0.0, 90.0)
    calculate = st.button("🔍 Calculate")
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

# --- Slope Gradient ---
elif tool == "Slope Gradient (%)":
    st.subheader("⛰️ Slope Gradient (%)")
    rise = st.number_input("Vertical Rise (m)", 0.0)
    run = st.number_input("Horizontal Run (m)", 0.0)
    calculate = st.button("🔍 Calculate")
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

# --- Grain Size to Phi ---
elif tool == "Grain Size to Phi":
    st.subheader("🌾 Grain Size to Phi (φ)")
    size = st.number_input("Grain Size (mm)", 0.0)
    calculate = st.button("🔍 Calculate")
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
