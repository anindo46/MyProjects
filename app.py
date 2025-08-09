import streamlit as st
import math
import io
import requests
import numpy as np
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie

# Import the custom tool from the separate module file
from qfl_mia_tool import create_qfl_plot

# --- PAGE CONFIGURATION ---
# Set up the page layout, title, and icon. This should be the first Streamlit command.
st.set_page_config(
    page_title="GeoLab Pro | Geoscience Toolkit",
    layout="wide",
    page_icon="🌍"
)

# --- MODULES & APP STATE ---
# Define the available modules in a dictionary for easy management.
MODULES = {
    "QFL Ternary Plot": "qfl_tool",
    "Stereonet Plotter": "stereonet_plotter",
    "True Dip Calculator": "true_dip_calculator",
    "Porosity Calculator": "porosity_calculator",
    "Stratigraphic Thickness Estimator": "strat_thickness_estimator",
    "Slope Gradient Calculator": "slope_gradient",
    "Grain Size (mm to Φ)": "grain_size_to_phi"
}

# Initialize session state to keep track of the selected module.
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None

# --- HELPER FUNCTIONS ---

def load_lottie_url(url: str):
    """
    Fetches a Lottie JSON animation from a URL.
    Includes error handling for the web request.
    """
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()  # Raises an exception for bad status codes
        return r.json()
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not load animation: {e}")
        return None

def create_download_button(fig, filename: str):
    """
    Generates a download button for a Matplotlib figure.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', dpi=300)
    st.download_button(
        label="📥 Download Plot as PNG",
        data=buf.getvalue(),
        file_name=filename,
        mime="image/png"
    )

# --- UI MODULES ---
# Each function below corresponds to a tool in the app.

def qfl_tool_ui():
    """
    UI for the QFL Ternary Plot tool.
    """
    st.header("💎 QFL Ternary Plot for Sandstone Classification")
    st.markdown("""
    This tool plots sandstone composition on a Quartz-Feldspar-Lithic fragment (QFL) ternary diagram. 
    Enter the percentages of Q, F, and L to classify your sample based on **Pettijohn's (1975)** classification scheme.
    """)

    with st.form("qfl_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            q = st.number_input("Quartz (%)", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
        with col2:
            f = st.number_input("Feldspar (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
        with col3:
            l = st.number_input("Lithic Fragments (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0)

        submitted = st.form_submit_button("📊 Plot QFL Diagram")

    if submitted:
        total = q + f + l
        if not math.isclose(total, 100.0, rel_tol=1e-5):
            st.error(f"The sum of Q, F, and L must be 100%. Current sum is {total:.2f}%. Please adjust the values.")
        else:
            with st.spinner("Generating interactive plot..."):
                fig = create_qfl_plot(q, f, l)
                st.plotly_chart(fig, use_container_width=True)


def stereonet_plotter_ui():
    """
    UI for the Stereonet Plotter.
    Correctly plots planes (as great circles) and lines (as points).
    """
    st.header("🧭 Stereonet Plotter")
    st.markdown("Visualize planes and lines on an equal-area (Schmidt) lower-hemisphere stereonet.")

    with st.form("stereonet_form"):
        st.subheader("Plane")
        col1, col2 = st.columns(2)
        with col1:
            strike = st.number_input("Strike of Plane (°)", 0.0, 360.0, value=30.0)
        with col2:
            dip = st.number_input("Dip of Plane (°)", 0.0, 90.0, value=45.0)

        st.subheader("Lineation")
        col3, col4 = st.columns(2)
        with col3:
            trend = st.number_input("Trend of Line (°)", 0.0, 360.0, value=150.0)
        with col4:
            plunge = st.number_input("Plunge of Line (°)", 0.0, 90.0, value=25.0)

        submitted = st.form_submit_button("🔍 Plot Stereonet")

    if submitted:
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_rlim(0, 1)
        ax.set_yticklabels([])
        ax.grid(True)
        ax.set_title("Lower-Hemisphere Equal-Area Stereonet", pad=20)

        # Plot Plane as a Great Circle
        strike_rad = np.deg2rad(strike)
        dip_rad = np.deg2rad(dip)
        pole_trend_rad = strike_rad - np.pi / 2
        pole_plunge_rad = np.pi / 2 - dip_rad
        
        g, d = np.meshgrid(np.linspace(0, 2 * np.pi, 360), np.linspace(0, np.pi/2, 90))
        X = np.sin(g) * np.tan(d/2)
        Y = np.cos(g) * np.tan(d/2)
        
        great_circle_theta = np.linspace(0, 2 * np.pi, 360)
        great_circle_r = np.tan(np.pi/4 - dip_rad/2) * np.cos(great_circle_theta - (strike_rad - np.pi/2))
        
        # We need to calculate the great circle path correctly
        dip_direction_rad = strike_rad + np.pi / 2
        alpha = np.linspace(-np.pi/2, np.pi/2, 100)
        trend_great_circle = dip_direction_rad + np.arctan(np.tan(alpha) / np.cos(dip_rad))
        plunge_great_circle = np.arcsin(np.sin(alpha) * np.sin(dip_rad))
        
        # Convert to polar coordinates for plotting
        r_plane = np.tan(np.pi/4 - plunge_great_circle/2)
        theta_plane = trend_great_circle
        
        ax.plot(theta_plane, r_plane, label=f'Plane ({strike:.0f}/{dip:.0f})', color='b')

        # Plot Line as a Point
        trend_rad = np.deg2rad(trend)
        plunge_rad = np.deg2rad(plunge)
        r_line = np.tan(np.pi/4 - plunge_rad/2)
        ax.plot(trend_rad, r_line, 'ro', markersize=8, label=f'Line ({trend:.0f}/{plunge:.0f})')

        ax.legend()
        st.pyplot(fig)
        create_download_button(fig, "stereonet_plot.png")


def true_dip_calculator_ui():
    """
    UI for the True Dip Calculator.
    """
    st.header("📐 True Dip from Apparent Dips")
    st.markdown("Calculate the true dip of a plane from an apparent dip measurement and the angle to the true dip direction.")

    with st.form("truedip_form"):
        apparent_dip = st.number_input("Apparent Dip (°)", min_value=0.0, max_value=90.0, value=30.0)
        angle_diff = st.number_input("Angle Between Strike and Traverse (°)", min_value=0.1, max_value=90.0, value=45.0)
        submitted = st.form_submit_button("🔍 Calculate True Dip")

    if submitted:
        true_dip = math.degrees(math.atan(math.tan(math.radians(apparent_dip)) / math.sin(math.radians(angle_diff))))
        st.success(f"**Calculated True Dip: {true_dip:.2f}°**")
        st.latex(r"\text{True Dip} = \arctan\left(\frac{\tan(\text{Apparent Dip})}{\sin(\text{Angle Difference})}\right)")


def porosity_calculator_ui():
    """
    UI for the Porosity Calculator.
    """
    st.header("🪨 Rock Porosity Calculator")
    st.markdown("Calculate the porosity of a rock sample from its pore volume and total bulk volume.")

    with st.form("porosity_form"):
        pore_volume = st.number_input("Pore Volume (e.g., cm³)", min_value=0.0, value=25.0)
        total_volume = st.number_input("Total Bulk Volume (e.g., cm³)", min_value=0.0, value=100.0)
        submitted = st.form_submit_button("🔍 Calculate Porosity")

    if submitted:
        if total_volume == 0:
            st.error("Total Bulk Volume must be greater than 0.")
        else:
            porosity = (pore_volume / total_volume) * 100
            st.success(f"**Calculated Porosity: {porosity:.2f}%**")
            st.latex(r"\text{Porosity (\%)} = \left(\frac{\text{Pore Volume}}{\text{Total Volume}}\right) \times 100")


def strat_thickness_ui():
    """
    UI for the Stratigraphic Thickness Estimator.
    """
    st.header("📏 Stratigraphic Thickness Estimator")
    st.markdown("Calculate the true thickness of a stratigraphic layer based on measured thickness and dip angle.")

    with st.form("thickness_form"):
        measured_thickness = st.number_input("Measured Thickness (units)", min_value=0.0, value=50.0)
        dip_angle = st.number_input("Dip Angle (°)", min_value=0.0, max_value=90.0, value=30.0)
        submitted = st.form_submit_button("🔍 Calculate True Thickness")

    if submitted:
        true_thickness = measured_thickness * math.sin(math.radians(dip_angle))
        st.success(f"**True Stratigraphic Thickness: {true_thickness:.2f} units**")
        st.latex(r"\text{True Thickness} = \text{Measured Thickness} \times \sin(\text{Dip Angle})")


def slope_gradient_ui():
    """
    UI for the Slope Gradient Calculator.
    """
    st.header("⛰️ Slope Gradient Calculator")
    st.markdown("Calculate the slope gradient as a percentage from vertical rise and horizontal run.")

    with st.form("slope_form"):
        rise = st.number_input("Vertical Rise (units)", min_value=0.0, value=10.0)
        run = st.number_input("Horizontal Run (units)", min_value=0.0, value=100.0)
        submitted = st.form_submit_button("🔍 Calculate Slope Gradient")

    if submitted:
        if run == 0:
            st.error("Horizontal Run must be greater than 0.")
        else:
            slope = (rise / run) * 100
            st.success(f"**Slope Gradient: {slope:.2f}%**")
            st.latex(r"\text{Slope Gradient (\%)} = \left(\frac{\text{Vertical Rise}}{\text{Horizontal Run}}\right) \times 100")


def grain_size_to_phi_ui():
    """
    UI for the Grain Size to Phi converter.
    """
    st.header("🌾 Grain Size (mm) to Phi (φ) Converter")
    st.markdown("Convert grain size from millimeters to the logarithmic Phi (φ) scale.")

    with st.form("phi_form"):
        grain_size_mm = st.number_input("Grain Size (mm)", min_value=0.0001, value=1.0, format="%.4f")
        submitted = st.form_submit_button("🔍 Calculate Phi (φ)")

    if submitted:
        phi_value = -math.log2(grain_size_mm)
        st.success(f"**Phi (φ) Value: {phi_value:.2f} φ**")
        st.latex(r"\phi = -\log_2(\text{Grain Size in mm})")

# --- NAVIGATION & MAIN APP LAYOUT ---

def display_homepage():
    """
    Displays the main welcome page of the application.
    """
    st.markdown("""
    <style>
        .home-title {
            font-size: 3.5rem; font-weight: 700; color: #1E90FF; text-align: center;
        }
        .home-subtitle {
            font-size: 1.5rem; color: #4F4F4F; text-align: center; margin-bottom: 2rem;
        }
        .feature-list {
            font-size: 1.1rem; margin-top: 1rem; list-style-position: inside; text-align: left;
        }
    </style>
    """, unsafe_allow_html=True)

    lottie_earth = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_3ntisyuc.json")

    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        if lottie_earth:
            st_lottie(lottie_earth, height=350, speed=1, loop=True)
        else:
            st.image("https://placehold.co/400x400/1E90FF/FFFFFF?text=GeoLab\nPro", use_column_width=True)

    with col2:
        st.markdown('<h1 class="home-title">Welcome to GeoLab Pro</h1>', unsafe_allow_html=True)
        st.markdown('<p class="home-subtitle">Your Professional Toolkit for Geoscience</p>', unsafe_allow_html=True)
        st.markdown("""
        **GeoLab Pro** is designed for geology students and professionals, offering a suite of powerful and easy-to-use tools for common geological calculations and visualizations.
        <ul class="feature-list">
            <li>✔️ Instant and accurate geological calculations.</li>
            <li>✔️ Interactive and downloadable plots.</li>
            <li>✔️ User-friendly interface for students and researchers.</li>
        </ul>
        <br>
        Select a module from the sidebar to begin your analysis.
        """, unsafe_allow_html=True)

def main():
    """
    Main function to run the Streamlit app.
    Handles page routing and layout.
    """
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("GeoLab Pro")
    st.sidebar.markdown("---")
    
    # Home button
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.selected_module = None
        st.rerun() # Use st.rerun() instead of deprecated experimental_rerun

    st.sidebar.subheader("Analysis Modules")
    
    # Module selection buttons
    for display_name, mod_id in MODULES.items():
        if st.sidebar.button(display_name, use_container_width=True):
            st.session_state.selected_module = mod_id
            st.rerun()

    # --- MAIN PANEL DISPLAY ---
    if st.session_state.selected_module is None:
        display_homepage()
    else:
        # A dictionary mapping module_id to its UI function
        ui_function_map = {
            "qfl_tool": qfl_tool_ui,
            "stereonet_plotter": stereonet_plotter_ui,
            "true_dip_calculator": true_dip_calculator_ui,
            "porosity_calculator": porosity_calculator_ui,
            "strat_thickness_estimator": strat_thickness_ui,
            "slope_gradient": slope_gradient_ui,
            "grain_size_to_phi": grain_size_to_phi_ui,
        }
        # Get the function from the map and call it
        selected_function = ui_function_map.get(st.session_state.selected_module)
        if selected_function:
            selected_function()

    # --- FOOTER ---
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; font-size:12px; color:gray; padding:10px;">
        Developed with ❤️ by <b>Anindo Paul Sourav</b><br>
        Department of Geology and Mining, University of Barishal
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
