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
        
        .title-bar { 
            display: flex; 
            align-items: center; 
            gap: 15px; 
            margin-bottom: 10px; 
            animation: slideIn 1s ease-out;
        }
        
        .title-bar img { 
            width: 50px; 
            animation: zoomIn 1s ease-out;
        }
        
        .title-bar h2 { 
            margin: 0; 
            font-family: 'Arial', sans-serif; 
            color: #333;
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
            margin-top: 80px;
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

        /* Icon Animations */
        .icon-container {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 30px;
            animation: fadeInUp 3s ease-out;
        }

        .icon-container img {
            width: 60px;
            height: 60px;
            animation: bounce 2s infinite;
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

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
    </style>
""", unsafe_allow_html=True)

# --- Welcome Section ---
st.markdown("""
    <div class="welcome-section">
        <div class="welcome-title">Welcome to GeoLab Pro</div>
        <div class="welcome-subtitle">Your all-in-one Geoscience Toolkit for Research and Exploration</div>
        
        <div class="icon-container">
            <img src="https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png" alt="Research Icon">
            <img src="https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png" alt="Upload Icon">
            <img src="https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png" alt="Analysis Icon">
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🧪 GeoLab Pro")
st.sidebar.info("A Smart Geoscience Toolkit by Anindo Paul Sourav\n\nUniversity of Barishal")
st.sidebar.markdown("---")
st.sidebar.caption("🔍 Choose a tool from the selector below")

# --- Title and Credit ---
st.markdown("""
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
    "Stereonet Plotter",  # Moved this to the first position
    "True Dip Calculator",
    "Porosity Calculator",
    "Stratigraphic Thickness Estimator",
    "Slope Gradient (%)",
    "Grain Size to Phi"
])

# --- Sidebar Descriptions ---
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

# --- Continue with other tools...
