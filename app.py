
import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import io

st.set_page_config(page_title="GeoLab Pro", layout="centered")

# --- Logo and Title ---
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:15px;">
        <img src="https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/pngwing.com.png" width="50">
        <div>
            <h2 style="margin:0;">GeoLab Pro</h2>
            <p style="margin:0;">A Smart Geoscience Toolkit by <strong>Anindo Paul Sourav</strong> | University of Barishal</p>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# --- Tool Selector ---
tool = st.selectbox("Choose a Tool / একটি টুল বেছে নিন:", [
    "True Dip Calculator",
    "Porosity Calculator",
    "Stratigraphic Thickness Estimator",
    "Slope Gradient (%)",
    "Grain Size to Phi"
])

# --- Helper: Show and Download Matplotlib Figure ---
def show_and_download(fig, filename="diagram.png"):
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.download_button(
        label="ðﾟﾓﾥ Download Diagram as PNG",
        data=buf.getvalue(),
        file_name=filename,
        mime="image/png"
    )

# --- True Dip Calculator ---
if tool == "True Dip Calculator":
    st.subheader("ðﾟﾓﾐ True Dip from Apparent Dip")
    ad = st.number_input("Apparent Dip (°)", 0.0)
    angle = st.number_input("Angle Between Directions (°)", 0.0, 90.0)
    calculate = st.button("Calculate True Dip")

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
    st.subheader("ðﾟﾪﾨ Porosity % from Volume")
    pores = st.number_input("Pore Volume (cm³)", 0.0)
    total = st.number_input("Total Volume (cm³)", 0.0)
    calculate = st.button("Calculate Porosity")

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
    st.subheader("ðﾟﾓﾏ Stratigraphic Thickness Estimation")
    measured = st.number_input("Measured Thickness (m)", 0.0)
    dip = st.number_input("Dip Angle (°)", 0.0, 90.0)
    calculate = st.button("Calculate True Thickness")

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
    calculate = st.button("Calculate Slope")

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
    st.subheader("ðﾟﾌﾾ Grain Size to Phi (φ)")
    size = st.number_input("Grain Size (mm)", 0.0)
    calculate = st.button("Convert to Phi")

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
