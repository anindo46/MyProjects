import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import io

# Page configuration
st.set_page_config(
    page_title="GeoLab Pro | Geoscience Toolkit",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🧪"
)

# Modules dictionary: key = display name, value = internal code
MODULES = {
    "MIA Tool": "mia_tool",
    "Stereonet Plotter": "stereonet_plotter",
    "True Dip Calculator": "true_dip_calculator",
    "Porosity Calculator": "porosity_calculator",
    "Stratigraphic Thickness Estimator": "stratigraphic_thickness_estimator",
    "Slope Gradient (%)": "slope_gradient",
    "Grain Size to Phi": "grain_size_to_phi"
}

# ----------- HELPER: Show & Download Plot ------------
def show_and_download(fig, filename="diagram.png"):
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.download_button(
        label="Download Diagram as PNG",
        data=buf.getvalue(),
        file_name=filename,
        mime="image/png"
    )

# ----------- MODULE IMPLEMENTATIONS ------------------

def mia_tool():
    st.header("MIA Tool")
    st.info("MIA Tool is under development. Stay tuned!")

def stereonet_plotter():
    st.header("Stereonet Plotter")
    strike = st.number_input("Strike (°)", 0.0, 360.0)
    dip = st.number_input("Dip (°)", 0.0, 90.0)
    trend = st.number_input("Trend (°)", 0.0, 360.0)
    plunge = st.number_input("Plunge (°)", 0.0, 90.0)
    if st.button("Plot Stereonet"):
        strike_rad = math.radians(strike)
        dip_rad = math.radians(dip)
        trend_rad = math.radians(trend)
        plunge_rad = math.radians(plunge)

        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111, projection='polar')
        ax.plot([strike_rad, strike_rad + math.pi], [dip_rad, dip_rad], label="Plane", color="blue")
        ax.plot([trend_rad, trend_rad + math.pi], [plunge_rad, plunge_rad], label="Line", color="red")
        ax.set_title("Stereonet")
        ax.legend()
        show_and_download(fig, "stereonet_plot.png")

def true_dip_calculator():
    st.header("True Dip Calculator")
    apparent_dip = st.number_input("Apparent Dip (°)", 0.0)
    angle = st.number_input("Angle Between Directions (°)", 0.0, 90.0)
    if st.button("Calculate True Dip"):
        if angle == 0:
            st.error("Angle must be greater than 0")
        else:
            true_dip = math.degrees(math.atan(math.tan(math.radians(apparent_dip)) / math.sin(math.radians(angle))))
            st.success(f"True Dip: {true_dip:.2f}°")

def porosity_calculator():
    st.header("Porosity Calculator")
    pore_vol = st.number_input("Pore Volume (cm³)", 0.0)
    total_vol = st.number_input("Total Volume (cm³)", 0.0)
    if st.button("Calculate Porosity"):
        if total_vol == 0:
            st.error("Total volume must be greater than 0")
        else:
            porosity = (pore_vol / total_vol) * 100
            st.success(f"Porosity: {porosity:.2f}%")

def stratigraphic_thickness_estimator():
    st.header("Stratigraphic Thickness Estimator")
    measured_thickness = st.number_input("Measured Thickness (m)", 0.0)
    dip_angle = st.number_input("Dip Angle (°)", 0.0, 90.0)
    if st.button("Calculate True Thickness"):
        true_thickness = measured_thickness * math.sin(math.radians(dip_angle))
        st.success(f"True Thickness: {true_thickness:.2f} m")

def slope_gradient():
    st.header("Slope Gradient Calculator")
    vertical_rise = st.number_input("Vertical Rise (m)", 0.0)
    horizontal_run = st.number_input("Horizontal Run (m)", 0.0)
    if st.button("Calculate Slope Gradient"):
        if horizontal_run == 0:
            st.error("Horizontal run must be greater than 0")
        else:
            slope = (vertical_rise / horizontal_run) * 100
            st.success(f"Slope Gradient: {slope:.2f}%")

def grain_size_to_phi():
    st.header("Grain Size to Phi (φ) Calculator")
    grain_size = st.number_input("Grain Size (mm)", 0.0)
    if st.button("Calculate Phi"):
        if grain_size <= 0:
            st.error("Grain size must be greater than 0")
        else:
            phi = -math.log2(grain_size)
            st.success(f"Phi (φ) = {phi:.2f}")

# ----------- DISPLAY HOME PAGE ------------------------

def display_homepage():
    st.title("Welcome to GeoLab Pro")
    st.write(
        """
        A clean, simple, and professional geoscience toolkit.
        
        Select a module below to begin your analysis.
        """
    )
    module = st.selectbox("Select a Module", list(MODULES.keys()))
    if st.button("Start"):
        st.session_state.selected_module = MODULES[module]
        st.experimental_rerun()

# ----------- SIDEBAR WITH MODULE NAVIGATION -------------

def sidebar_navigation():
    st.sidebar.title("Modules")
    current_module = st.session_state.selected_module

    selected = st.sidebar.selectbox(
        "Switch Module",
        list(MODULES.keys()),
        index=list(MODULES.values()).index(current_module)
    )
    if MODULES[selected] != current_module:
        st.session_state.selected_module = MODULES[selected]
        st.experimental_rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("Back to Home"):
        st.session_state.selected_module = None
        st.experimental_rerun()

# ----------- MAIN APP LOGIC -----------------------------

def main():
    if "selected_module" not in st.session_state:
        st.session_state.selected_module = None

    if st.session_state.selected_module is None:
        display_homepage()
    else:
        sidebar_navigation()

        # Call the right module UI function
        mod = st.session_state.selected_module
        if mod == "mia_tool":
            mia_tool()
        elif mod == "stereonet_plotter":
            stereonet_plotter()
        elif mod == "true_dip_calculator":
            true_dip_calculator()
        elif mod == "porosity_calculator":
            porosity_calculator()
        elif mod == "stratigraphic_thickness_estimator":
            stratigraphic_thickness_estimator()
        elif mod == "slope_gradient":
            slope_gradient()
        elif mod == "grain_size_to_phi":
            grain_size_to_phi()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; color:gray; font-size:12px; padding:10px 0;">
            Developed by Anindo Paul Sourav — University of Barishal
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
