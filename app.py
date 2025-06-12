import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import io
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="GeoLab Pro", layout="wide", page_icon="🧪")

# --- Custom CSS for Premium Animation and Style ---
st.markdown("""
    <style>
        /* General Styling */
        body { 
            font-family: 'Arial', sans-serif; 
            background-color: #f4f4f4;
            animation: fadeIn 1s ease-out;
        }

        /* Title Section */
        .title-bar { 
            text-align: center;
            margin-top: 20px;
            animation: fadeInUp 1.5s ease-out;
        }
        
        .title-bar h2 { 
            font-family: 'Arial', sans-serif; 
            color: #006B3F;
            font-size: 40px;
            font-weight: bold;
        }

        .credit { 
            font-size: 14px; 
            color: gray; 
            margin-top: -10px; 
            font-family: 'Arial', sans-serif; 
        }

        /* Welcome Section Animations */
        .welcome-section {
            text-align: center;
            padding: 50px;
            margin-top: 30px;
            animation: fadeInUp 2s ease-out;
        }

        .welcome-title {
            font-size: 36px;
            font-weight: bold;
            color: #006B3F;
            animation: fadeInUp 2s ease-out;
        }

        .welcome-subtitle {
            font-size: 18px;
            margin-top: 10px;
            color: #333;
            animation: fadeInUp 2.5s ease-out;
        }

        /* Tool Selector Container */
        .tool-selector {
            display: flex;
            justify-content: center;
            margin-top: 30px;
            animation: fadeInUp 3s ease-out;
        }

        .tool-selector select {
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            border: 2px solid #ddd;
            transition: all 0.3s ease;
        }

        /* Button Hover Effect */
        .stButton, .stSelectbox, .stSlider {
            transition: transform 0.3s ease, background-color 0.3s ease;
        }
        
        .stButton:hover { 
            background-color: #4CAF50; 
            transform: scale(1.1);
        }

        /* Fade-in and Zoom-in Animation */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes zoomIn {
            from { transform: scale(0.5); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        @keyframes slideIn {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
        }
    </style>
""", unsafe_allow_html=True)

# --- Welcome Section ---
st.markdown("""
    <div class="welcome-section">
        <div class="welcome-title">Welcome to GeoLab Pro</div>
        <div class="welcome-subtitle">Your all-in-one Geoscience Toolkit for Research and Exploration</div>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🧪 GeoLab Pro")
st.sidebar.info("A Smart Geoscience Toolkit by Anindo Paul Sourav\n\nUniversity of Barishal")
st.sidebar.markdown("---")
st.sidebar.caption("🔍 Choose a tool from the selector below")

# --- Personal Information in Sidebar ---
st.sidebar.markdown("### About Me")
st.sidebar.markdown("""
    - **Name**: Anindo Paul Sourav
    - **Field**: Geology and Mining, University of Barishal
    - **Email**: [anindo.glm@gmail.com](mailto:anindo.glm@gmail.com)
    - **Portfolio**: [My Portfolio](https://anindo46.github.io/portfolio/)
    - **Phone**: (+880) 1701026866
    - **LinkedIn**: [Anindo LinkedIn](https://www.linkedin.com/in/anindo046/)
""")

# --- Tool Selector ---
tool = st.selectbox("Choose a Tool / একটি টুল বেছে নিন:", [
    "Stereonet Plotter",  # Moved this to the first position
    "True Dip Calculator",
    "Porosity Calculator",
    "Stratigraphic Thickness Estimator",
    "Slope Gradient (%)",
    "Grain Size to Phi"
])

# --- Tool Descriptions ---
st.sidebar.markdown("### Tool Descriptions")

# Stereonet Plotter Description
if tool == "Stereonet Plotter":
    st.sidebar.markdown("""
    **Stereonet Plotter** / **স্টেরিওনেট প্লটার**:
    - This tool allows you to plot planes and lines on a stereonet by entering the strike & dip for planes and trend & plunge for lines.
    - **Example**: 
      - Strike = 30°, Dip = 45° for a plane.
      - Trend = 90°, Plunge = 30° for a line.
    - The plot will show the relationships between these structures, useful for structural geology and fault/fold analysis.
    """)

# True Dip Calculator Description
elif tool == "True Dip Calculator":
    st.sidebar.markdown("""
    **True Dip Calculator** / **ট্রু ডিপ ক্যালকুলেটর**:
    - This tool calculates the true dip of a geological plane when the apparent dip and the angle between directions are given.
    - **Example**: If the apparent dip of a plane is 30° and the angle between directions is 45°, the tool will calculate the true dip.
    - **Usage**: Useful for structural geology, measuring the true angle of rock layers.
    """)

# Porosity Calculator Description
elif tool == "Porosity Calculator":
    st.sidebar.markdown("""
    **Porosity Calculator** / **পোরোসিটি ক্যালকুলেটর**:
    - This tool calculates the porosity percentage of a rock sample given the pore volume and the total volume.
    - **Example**: If a rock sample has 50 cm³ of pore space and a total volume of 100 cm³, the porosity will be 50%.
    - **Usage**: Commonly used in petrology, hydrogeology, and reservoir engineering.
    """)

# Stratigraphic Thickness Estimator Description
elif tool == "Stratigraphic Thickness Estimator":
    st.sidebar.markdown("""
    **Stratigraphic Thickness Estimator** / **স্ট্র্যাটিগ্রাফিক থিকনেস এসটিমেটর**:
    - This tool helps estimate the true thickness of a stratigraphic layer based on the measured thickness and dip angle.
    - **Example**: If the measured thickness of a layer is 50 meters and the dip angle is 30°, the true thickness will be calculated.
    - **Usage**: Useful for geological mapping and resource estimation.
    """)

# Slope Gradient Description
elif tool == "Slope Gradient (%)":
    st.sidebar.markdown("""
    **Slope Gradient (%)** / **স্লোপ গ্রেডিয়েন্ট (%)**:
    - This tool calculates the gradient of a slope (as a percentage) using the vertical rise and horizontal run.
    - **Example**: If the vertical rise is 10 meters and the horizontal run is 50 meters, the slope gradient will be 20%.
    - **Usage**: This tool is used in geomorphology, civil engineering, and environmental studies.
    """)

# Grain Size to Phi Description
elif tool == "Grain Size to Phi":
    st.sidebar.markdown("""
    **Grain Size to Phi (φ)** / **গ্রেইন সাইজ থেকে ফি (φ)**:
    - This tool calculates the phi (φ) scale of a grain size in millimeters.
    - **Example**: If a grain size is 2 mm, the phi value will be calculated as φ = -log₂(2) = 1.
    - **Usage**: Used in sedimentology to classify grain sizes for particle size analysis.
    """)

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

# --- Continue with Tool Logic (Stereonet Plotter, True Dip Calculator, etc.)
# --- Continue with Tool Logic (Stereonet Plotter, True Dip Calculator, etc.)

# --- Continue with Tool Logic (Stereonet Plotter, True Dip Calculator, etc.)

# --- Stereonet Plotter ---
if tool == "Stereonet Plotter":
    st.subheader("🧭 Stereonet Plotter")
    
    # Input Fields
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

# --- Continue with other tools (True Dip Calculator, Porosity Calculator, etc.)
# --- True Dip Calculator ---
if tool == "True Dip Calculator":
    st.subheader("🧭 True Dip from Apparent Dip")
    
    # Input Fields
    ad = st.number_input("Apparent Dip (°)", min_value=0.0, max_value=90.0, step=0.1)
    angle = st.number_input("Angle Between Directions (°)", min_value=0.0, max_value=90.0, step=0.1)
    
    calculate = st.button("🔍 Calculate True Dip")
    
    if calculate:
        # Calculation of True Dip
        td = math.degrees(math.atan(math.tan(math.radians(ad)) / math.sin(math.radians(angle))))
        st.success(f"✅ True Dip = {td:.2f}°")
        st.markdown(r"**Formula:** True Dip = tan⁻¹(tan(Apparent Dip) / sin(Angle))")
        
        # Plotting Diagram
        fig, ax = plt.subplots(figsize=(6, 6))
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
    
    # Input Fields
    pores = st.number_input("Pore Volume (cm³)", min_value=0.0)
    total = st.number_input("Total Volume (cm³)", min_value=0.0)
    
    calculate = st.button("🔍 Calculate Porosity")
    
    if calculate and total > 0:
        porosity = (pores / total) * 100
        solid = total - pores
        st.success(f"✅ Porosity = {porosity:.2f}%")
        st.markdown(r"**Formula:** Porosity = (Pore Volume / Total Volume) × 100")
        
        # Plotting Porosity Distribution
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
    
    # Input Fields
    measured = st.number_input("Measured Thickness (m)", min_value=0.0)
    dip = st.number_input("Dip Angle (°)", min_value=0.0, max_value=90.0)
    
    calculate = st.button("🔍 Calculate True Thickness")
    
    if calculate and dip > 0:
        true_thick = measured * math.sin(math.radians(dip))
        st.success(f"✅ True Thickness = {true_thick:.2f} m")
        st.markdown(r"**Formula:** True Thickness = Measured × sin(Dip)")
        
        # Plotting Thickness Diagram
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot([0, 1], [0, measured], 'saddlebrown', lw=3, label='Measured')
        ax.plot([0, 1], [0, true_thick], 'limegreen', lw=3, label='True')
        ax.legend()
        ax.set_title("Measured vs True Thickness")
        ax.set_ylabel("Thickness (m)")
        show_and_download(fig, "stratigraphy_diagram.png")

# --- Slope Gradient (%) ---
elif tool == "Slope Gradient (%)":
    st.subheader("⛰️ Slope Gradient (%)")
    
    # Input Fields
    rise = st.number_input("Vertical Rise (m)", min_value=0.0)
    run = st.number_input("Horizontal Run (m)", min_value=0.0)
    
    calculate = st.button("🔍 Calculate Slope Gradient")
    
    if calculate and run > 0:
        slope = (rise / run) * 100
        st.success(f"✅ Slope Gradient = {slope:.2f}%")
        st.markdown(r"**Formula:** Slope % = (Rise / Run) × 100")
        
        # Plotting Slope Profile
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot([0, run], [0, 0], 'k--')
        ax.plot([0, run], [0, rise], 'b-', lw=2)
        ax.fill([0, run, run], [0, 0, rise], color='skyblue', alpha=0.3)
        ax.text(run/2, rise/2, f"{slope:.1f}%", fontsize=12, ha='center')
        ax.set_xlim(0, run + 5)
        ax.set_ylim(0, rise + 5)
        ax.set_title("Slope Profile")
        ax.axis('off')
        show_and_download(fig, "slope_diagram.png")

# --- Grain Size to Phi ---
elif tool == "Grain Size to Phi":
    st.subheader("🌾 Grain Size to Phi (φ)")
    
    # Input Fields
    size = st.number_input("Grain Size (mm)", min_value=0.0)
    
    calculate = st.button("🔍 Calculate Phi (φ)")
    
    if calculate and size > 0:
        phi = -math.log2(size)
        st.success(f"✅ φ = {phi:.2f}")
        st.markdown(r"**Formula:** φ = -log₂(Grain Size in mm)")
        
        # Plotting Grain Size vs Phi
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot([size], [phi], marker='o', markersize=10, color='crimson')
        ax.set_xlabel("Grain Size (mm)")
        ax.set_ylabel("Phi (φ)")
        ax.set_title("Grain Size → φ Scale")
        ax.grid(True)
        show_and_download(fig, "phi_diagram.png")
