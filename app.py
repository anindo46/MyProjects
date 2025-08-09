import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import io
from mpl_toolkits.mplot3d import Axes3D
from streamlit_lottie import st_lottie
import requests

# --- Page Config ---
st.set_page_config(
    page_title="GeoLab Pro | By Anindo Paul Sourav",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧪"
)

# --- Load Lottie helper ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Sidebar ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=120)
    st.markdown("### 🧪 GeoLab Pro")
    st.caption("By **Anindo Paul Sourav**  \nStudent, Geology and Mining, University of Barishal")
    st.markdown("---")
    
    tool = st.selectbox("📦 Choose a Tool", [
        "📊 MIA Tool",  # Your new MIA tool, first in list
        "🧭 Stereonet Plotter",
        "🧭 True Dip Calculator",
        "🪨 Porosity Calculator",
        "📏 Stratigraphic Thickness Estimator",
        "⛰️ Slope Gradient (%)",
        "🌾 Grain Size to Phi"
    ])

    st.markdown("---")
    st.markdown("""
    <p style='font-size:14px; color:#666;'>💡 Tip: Enter required inputs and generate your diagrams easily.</p>
    """, unsafe_allow_html=True)

# --- Homepage ---
def display_home():
    col1, col2 = st.columns([1, 2])
    with col1:
        lottie = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_w98qte06.json")
        if lottie:
            st_lottie(lottie, speed=1, loop=True, height=250)
        else:
            st.image("https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png", width=200)
    with col2:
        st.markdown("<h1 style='color:#4B8BBE;'>Welcome to GeoLab Pro</h1>", unsafe_allow_html=True)
        st.markdown("""
        <p style='font-size:18px;'>Your smart geoscience toolkit for advanced structural and sedimentological analysis.</p>
        <ul>
            <li>📥 Upload data and input parameters easily</li>
            <li>📊 Generate interactive plots and calculations</li>
            <li>📂 Export results as images or reports</li>
        </ul>
        """, unsafe_allow_html=True)
    st.success("👈 Select a tool from the sidebar to get started!")

# --- Routing ---
if tool == "📊 MIA Tool":
    st.subheader("📊 MIA Tool")
    st.info("MIA Tool module will be added here.")  # Placeholder for your MIA tool code

elif tool == "🧭 Stereonet Plotter":
    # Your existing stereonet plotter code here...
    # (Copy your current stereonet plotter code block without changes)
    pass

elif tool == "🧭 True Dip Calculator":
    # Your True Dip Calculator code here...
    pass

elif tool == "🪨 Porosity Calculator":
    # Your Porosity Calculator code here...
    pass

elif tool == "📏 Stratigraphic Thickness Estimator":
    # Your Stratigraphic Thickness code here...
    pass

elif tool == "⛰️ Slope Gradient (%)":
    # Your Slope Gradient code here...
    pass

elif tool == "🌾 Grain Size to Phi":
    # Your Grain Size to Phi code here...
    pass

else:
    display_home()
