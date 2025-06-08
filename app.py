import streamlit as st
import math

# --- Page setup ---
st.set_page_config(page_title="GeoLab Pro – Geology Toolkit", layout="wide")

# --- Logo + Header ---
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/University_of_Barishal_logo.svg/800px-University_of_Barishal_logo.svg.png", width=100)

st.markdown("""
<style>
.big-title {
    font-size:40px !important;
    font-weight: bold;
}
.subtitle {
    font-size:18px !important;
    color: gray;
}
.footer {
    font-size:14px !important;
    text-align: center;
    color: #888;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">GeoLab Pro – Geology Toolkit</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A Smart, Bilingual Toolkit for Geology Students</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Developed by Anindo Paul Sourav | University of Barishal</div>', unsafe_allow_html=True)

st.markdown("---")

# --- Language toggle ---
language = st.radio("🌐 Choose Language / ভাষা নির্বাচন করুন:", ["English", "বাংলা"])

# --- Sidebar tool selection ---
tool = st.sidebar.selectbox("🧭 Choose a Tool / একটি টুল বেছে নিন:", [
    "True Dip Calculator",
    "Grain Size to Phi",
    "Porosity Calculator",
    "Stratigraphic Thickness Estimator",
    "Slope Gradient (%)"
])

st.markdown(f"### {tool}")

# --- Language helper ---
def label(text_en, text_bn):
    return text_en if language == "English" else text_bn

# --- TOOL 1: True Dip ---
import math
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Optional bilingual label support
def label(en, bn=None):
    return en if bn is None else f"{en} / {bn}"

st.subheader(label("True Dip from Apparent Dip", "আপাত ডিপ থেকে সত্যিকারের ডিপ নির্ণয়"))

# Input values
ad = st.number_input(label("Apparent Dip (°)", "আপাত ডিপ (ডিগ্রি)"), min_value=0.0, max_value=90.0, step=0.1)
angle = st.number_input(label("Angle Between Directions (°)", "দিকের মধ্যকার কোণ (ডিগ্রি)"), min_value=0.0, max_value=90.0, step=0.1)

if st.button(label("Calculate", "হিসাব করুন")):
    # Calculation
    td = math.degrees(math.atan(math.tan(math.radians(ad)) / math.sin(math.radians(angle))))
    st.success(f"{label('True Dip', 'সত্যিকারের ডিপ')} = {td:.2f}°")
    
    # Formula Explanation
    st.markdown(r"**Formula:** True Dip = tan⁻¹(tan(Apparent Dip) / sin(Angle))")

    # Dynamic Triangle Plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    base = 1  # unit base length
    height = np.tan(np.radians(ad))  # apparent dip height

    x_coords = [0, base, base]
    y_coords = [0, 0, height]

    # Draw triangle
    ax.plot(x_coords + [0], y_coords + [0], 'k-', lw=2)
    ax.fill(x_coords + [0], y_coords + [0], 'lavender', alpha=0.4)

    # Labels
    ax.text(0.5, -0.1, f"Angle = {angle:.1f}°", ha='center', fontsize=9)
    ax.text(base + 0.1, height / 2, f"Apparent Dip = {ad:.1f}°", va='center', fontsize=9)
    ax.text(base / 2, height + 0.1, f"True Dip = {td:.2f}°", ha='center', fontsize=10, fontweight='bold')

    # Limits and remove axis
    ax.set_xlim(-0.2, 1.6)
    ax.set_ylim(-0.2, max(height + 0.5, 1))
    ax.axis('off')

    # Show in Streamlit
    st.pyplot(fig)


# --- TOOL 2: Phi Scale ---
elif tool == "Grain Size to Phi":
    st.subheader(label("Convert Grain Size to Phi (φ)", "শস্যের আকার থেকে ফাই (φ) নির্ণয়"))
    size = st.number_input(label("Grain Size (mm)", "শস্যের আকার (মিমি)"), min_value=0.001)
    if st.button(label("Convert", "রূপান্তর করুন")):
        phi = -math.log2(size)
        st.success(f"φ = {phi:.2f}")

# --- TOOL 3: Porosity ---
elif tool == "Porosity Calculator":
    st.subheader(label("Porosity % from Volume", "আয়তন থেকে পরোসিটি (%)"))
    pores = st.number_input(label("Pore Volume (cm³)", "ছিদ্রের আয়তন (সেমি³)"))
    total = st.number_input(label("Total Volume (cm³)", "মোট আয়তন (সেমি³)"))
    if total > 0 and st.button(label("Calculate", "হিসাব করুন")):
        porosity = (pores / total) * 100
        st.success(f"{label('Porosity', 'পরোসিটি')} = {porosity:.2f}%")

# --- TOOL 4: Thickness ---
elif tool == "Stratigraphic Thickness Estimator":
    st.subheader(label("Estimate True Thickness of a Bed", "একটি স্তরের প্রকৃত পুরুত্ব নির্ণয়"))
    obs_thickness = st.number_input(label("Measured Thickness (m)", "পরিমাপকৃত পুরুত্ব (মি)"))
    dip = st.number_input(label("Dip Angle (°)", "ডিপ কোণ (ডিগ্রি)"), 0.0, 90.0)
    if st.button(label("Calculate", "হিসাব করুন")):
        true_thick = obs_thickness * math.sin(math.radians(dip))
        st.success(f"{label('True Thickness', 'প্রকৃত পুরুত্ব')} = {true_thick:.2f} m")

# --- TOOL 5: Slope Gradient ---
elif tool == "Slope Gradient (%)":
    st.subheader(label("Slope Gradient", "ঢালের গ্রেডিয়েন্ট"))
    rise = st.number_input(label("Vertical Rise (m)", "উল্লম্ব উচ্চতা (মি)"))
    run = st.number_input(label("Horizontal Run (m)", "অনুভূমিক দূরত্ব (মি)"))
    if run > 0 and st.button(label("Calculate", "হিসাব করুন")):
        slope = (rise / run) * 100
        st.success(f"{label('Slope', 'ঢাল')} = {slope:.2f}%")

# --- Footer ---
st.markdown("---")
st.markdown(f'''
<div class="footer">
Developed by <b>Anindo Paul Sourav</b>
Department of Geology and Mining<br>
University of Barishal<br>
<br>
<a href="https://anindo46.github.io/portfolio/">MY PORTFOLIO</a><br>
Email: anindo.glm@gmail.com | 🌐 <a href="https://github.com/anindo46">GitHub</a>
</div>
''', unsafe_allow_html=True)
