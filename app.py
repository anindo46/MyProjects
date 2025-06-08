
import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

# --- Page setup ---
st.set_page_config(page_title="GeoLab Pro", layout="centered")

# --- Custom logo ---
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/University_of_Barishal_logo.svg/800px-University_of_Barishal_logo.svg.png", width=80)

# --- Title & credit ---
st.markdown("## ðﾟﾧﾪ GeoLab Pro")
st.markdown("#### Smart Geology Toolkit – Developed by **Anindo Paul Sourav** | University of Barishal")

# --- Tool selector ---
tool = st.selectbox("ðﾟﾎﾯ Choose a Tool / একটি টুল বেছে নিন:", [
    "True Dip Calculator",
    "Porosity Calculator",
    "Stratigraphic Thickness Estimator",
    "Slope Gradient (%)",
    "Grain Size to Phi"
])

# --- Tool: True Dip Calculator ---
if tool == "True Dip Calculator":
    st.subheader("ðﾟﾓﾐ True Dip from Apparent Dip / আপাত ডিপ থেকে সত্যিকারের ডিপ নির্ণয়")
    ad = st.number_input("Apparent Dip (°) / আপাত ডিপ (ডিগ্রি)", 0.0)
    angle = st.number_input("Angle Between Directions (°) / দিকের মধ্যকার কোণ (ডিগ্রি)", 0.0, 90.0)

    if st.button("Calculate True Dip"):
        td = math.degrees(math.atan(math.tan(math.radians(ad)) / math.sin(math.radians(angle))))
        st.success(f"✅ True Dip = {td:.2f}°")

        st.markdown(r"**Formula:** True Dip = tan⁻¹(tan(Apparent Dip) / sin(Angle))")

        # Draw triangle
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        b = 1
        h = np.tan(np.radians(ad))
        x = [0, b, b]
        y = [0, 0, h]
        ax.plot(x + [0], y + [0], 'k-', lw=2)
        ax.fill(x + [0], y + [0], 'lavender', alpha=0.4)
        ax.text(0.5, -0.1, f"Angle = {angle:.1f}°", ha='center')
        ax.text(b + 0.1, h / 2, f"Apparent = {ad}°", va='center')
        ax.text(b / 2, h + 0.1, f"True Dip = {td:.2f}°", ha='center', fontweight='bold')
        ax.axis('off')
        st.pyplot(fig)

# --- Tool: Porosity Calculator ---
elif tool == "Porosity Calculator":
    st.subheader("ðﾟﾪﾨ Porosity % from Volume / আয়তন থেকে পরোসিটি (%)")
    pores = st.number_input("Pore Volume (cm³)", min_value=0.0)
    total = st.number_input("Total Volume (cm³)", min_value=0.0)
    if total > 0 and st.button("Calculate Porosity"):
        porosity = (pores / total) * 100
        solid = total - pores
        st.success(f"✅ Porosity = {porosity:.2f}%")
        st.markdown(r"**Formula:** Porosity = (Pore Volume / Total Volume) × 100")

        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.barh(["Rock"], [pores], color='skyblue', label="Pore")
        ax.barh(["Rock"], [solid], left=[pores], color='saddlebrown', label="Solid")
        ax.set_xlim(0, total)
        ax.legend(loc="lower right")
        ax.set_facecolor('#f4f4f4')
        ax.get_yaxis().set_visible(False)
        ax.set_title("Porosity Distribution")
        st.pyplot(fig)

# --- Tool: Stratigraphic Thickness Estimator ---
elif tool == "Stratigraphic Thickness Estimator":
    st.subheader("ðﾟﾓﾏ Stratigraphic Thickness / স্তরের প্রকৃত পুরুত্ব নির্ণয়")
    obs = st.number_input("Measured Thickness (m)", 0.0)
    dip = st.number_input("Dip Angle (°)", 0.0, 90.0)
    if dip > 0 and st.button("Calculate True Thickness"):
        true_thick = obs * math.sin(math.radians(dip))
        st.success(f"✅ True Thickness = {true_thick:.2f} m")
        st.markdown(r"**Formula:** T = Measured × sin(Dip)")

# --- Tool: Slope Gradient Calculator ---
elif tool == "Slope Gradient (%)":
    st.subheader("⛰️ Slope Gradient / ঢালের গ্রেডিয়েন্ট")
    rise = st.number_input("Vertical Rise (m)", 0.0)
    run = st.number_input("Horizontal Run (m)", 0.0)
    if run > 0 and st.button("Calculate Slope"):
        slope = (rise / run) * 100
        st.success(f"✅ Slope = {slope:.2f}%")
        st.markdown(r"**Formula:** Slope % = (Rise / Run) × 100")

# --- Tool: Grain Size to Phi ---
elif tool == "Grain Size to Phi":
    st.subheader("ðﾟﾌﾾ Convert Grain Size to Phi (φ) / শস্যের আকার থেকে ফাই (φ)")
    size = st.number_input("Grain Size (mm) / শস্যের আকার (মিমি)", 0.0)
    if size > 0 and st.button("Convert to Phi"):
        phi = -math.log2(size)
        st.success(f"✅ φ = {phi:.2f}")
        st.markdown(r"**Formula:** φ = –log₂(Grain Size in mm)")
