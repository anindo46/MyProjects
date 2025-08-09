import streamlit as st
import math
import io
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from streamlit_lottie import st_lottie
import openai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GeoLab Pro | Geoscience Toolkit",
    layout="wide",
    page_icon="🌍"
)

# --- MODULES & APP STATE ---
MODULES = {
    "QFL & MIA Analysis": "qfl_mia_tool",
    "Stereonet Plotter": "stereonet_plotter",
    "True Dip Calculator": "true_dip_calculator",
    "Porosity Calculator": "porosity_calculator",
    "Stratigraphic Thickness Estimator": "strat_thickness_estimator",
    "Slope Gradient Calculator": "slope_gradient",
    "Grain Size (mm to Φ)": "grain_size_to_phi"
}

# Initialize session state variables
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'ai_report' not in st.session_state:
    st.session_state.ai_report = None
if 'ai_answer' not in st.session_state:
    st.session_state.ai_answer = None


# --- HELPER FUNCTIONS ---

def load_lottie_url(url: str):
    """Fetches a Lottie JSON animation from a URL with error handling."""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not load animation: {e}")
        return None

def create_download_button(fig, filename: str):
    """Generates a download button for a Matplotlib figure."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', dpi=300)
    st.download_button(
        label="📥 Download Plot as PNG",
        data=buf.getvalue(),
        file_name=filename,
        mime="image/png"
    )

# --- AI & QFL/MIA Functions ---

def get_ai_interpretation(api_key, df):
    """Calls OpenAI API to get a geological interpretation of the QFL/MIA data."""
    openai.api_key = api_key
    
    avg_q = df['Q_norm'].mean() * 100
    avg_f = df['F_norm'].mean() * 100
    avg_l = df['L_norm'].mean() * 100
    avg_mia = df['MIA'].mean()

    prompt = f"""
    You are an expert sedimentologist and petrographer providing an analysis for a geology student named Anindo Paul Sourav.
    I have analyzed {len(df)} sandstone samples. Here is the summary of the averaged data:
    - Average Quartz (Q): {avg_q:.2f}%
    - Average Feldspar (F): {avg_f:.2f}%
    - Average Lithic Fragments (L): {avg_l:.2f}%
    - Average Maturity Index of Arenites (MIA): {avg_mia:.2f}%

    Based on this data, please provide a comprehensive geological report in Markdown format. The report should be structured as follows:

    ### Geological Report

    **1. Executive Summary:**
    A brief overview of the key findings regarding provenance, tectonic setting, and weathering.

    **2. Provenance and Tectonic Setting Analysis:**
    Based on the average QFL values ({avg_q:.0f}/{avg_f:.0f}/{avg_l:.0f}), interpret the most likely tectonic setting by referencing the Dickinson (1983) model. Explain why the data points to a specific field (e.g., Craton Interior, Recycled Orogen, Basement Uplift, or Arc).

    **3. Weathering and Maturity Analysis:**
    Based on the average MIA value of {avg_mia:.2f}%, discuss the degree of chemical weathering and overall sediment maturity. Infer the likely climatic conditions (e.g., humid, arid, semi-arid) and relief of the source area.

    **4. Overall Conclusion:**
    Synthesize the provenance and maturity findings into a concluding paragraph that paints a complete picture of the sediment's history.

    ---

    ### Further Investigation Questions

    Finally, based on your interpretation, generate 2-3 specific, thought-provoking questions that a geologist like Anindo might ask next to further this investigation. These questions should prompt deeper thinking about the data.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert sedimentologist providing clear, educational geological reports."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred with the OpenAI API call: {e}"

def get_ai_answer(api_key, report, question):
    """Calls OpenAI API to answer a follow-up question based on a report."""
    openai.api_key = api_key

    prompt = f"""
    You are an expert sedimentologist acting as a teaching assistant for Anindo Paul Sourav.
    You have already provided the following geological report:
    ---
    {report}
    ---
    Now, please answer the following specific question based *only* on the context of the report you provided. Be concise and direct.

    Question: "{question}"
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful geological teaching assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred with the OpenAI API call: {e}"


def create_qfl_mia_plot(df):
    """Creates an interactive QFL ternary plot with Dickinson (1983) provenance fields."""
    fig = go.Figure()
    fields = {
        'Craton Interior': {'a': [1, 0.85, 0.95], 'b': [0, 0.15, 0], 'c': [0, 0, 0.05]},
        'Transitional Craton': {'a': [0.85, 0.60, 0.70, 0.95], 'b': [0.15, 0.40, 0.15, 0], 'c': [0, 0, 0.15, 0.05]},
        'Basement Uplift': {'a': [0.60, 0.70, 0.25, 0], 'b': [0.40, 0.15, 0.75, 1], 'c': [0, 0.15, 0, 0]},
        'Recycled Orogen': {'a': [0.75, 0.65, 0.55, 0.80], 'b': [0, 0.10, 0, 0], 'c': [0.25, 0.25, 0.45, 0.20]},
        'Transitional Arc': {'a': [0.55, 0.65, 0.15, 0], 'b': [0, 0.10, 0.60, 0.45], 'c': [0.45, 0.25, 0.25, 0.55]},
        'Dissected Arc': {'a': [0.25, 0.70, 0.15, 0], 'b': [0.75, 0.15, 0.60, 0.45], 'c': [0, 0.15, 0.25, 0.55]},
    }
    colors = {
        'Craton Interior': 'rgba(255, 228, 181, 0.6)', 'Transitional Craton': 'rgba(240, 230, 140, 0.6)',
        'Basement Uplift': 'rgba(218, 112, 214, 0.6)', 'Recycled Orogen': 'rgba(173, 216, 230, 0.6)',
        'Transitional Arc': 'rgba(144, 238, 144, 0.6)', 'Dissected Arc': 'rgba(255, 182, 193, 0.6)',
    }
    for name, coords in fields.items():
        fig.add_trace(go.Scatterternary({'mode': 'lines', 'a': coords['a'], 'b': coords['b'], 'c': coords['c'], 'fill': 'toself', 'fillcolor': colors[name], 'line': {'color': 'rgba(0,0,0,0.3)', 'width': 1}, 'name': name, 'hoverinfo': 'name'}))
    fig.add_trace(go.Scatterternary({'mode': 'markers', 'a': df['Q_norm'], 'b': df['F_norm'], 'c': df['L_norm'], 'marker': {'symbol': 'circle', 'color': 'black', 'size': 8, 'line': {'width': 1, 'color': 'white'}}, 'name': 'Your Samples', 'hovertemplate': '<b>Sample</b><br>Q: %{a:.1%}<br>F: %{b:.1%}<br>L: %{c:.1%}<extra></extra>'}))
    fig.update_layout({'ternary': {'sum': 1, 'aaxis': {'title': 'Q (Quartz)', 'min': 0, 'linewidth': 2, 'ticks': 'outside'}, 'baxis': {'title': 'F (Feldspar)', 'min': 0, 'linewidth': 2, 'ticks': 'outside'}, 'caxis': {'title': 'L (Lithic Fragments)', 'min': 0, 'linewidth': 2, 'ticks': 'outside'}}, 'title': {'text': "QFL Provenance Plot (Dickinson, 1983)", 'x': 0.5, 'font': {'size': 18}}, 'showlegend': True, 'legend': {'x': 1.1, 'y': 0.5}})
    return fig

def qfl_mia_tool_ui():
    """UI for the comprehensive QFL & MIA Analysis tool."""
    st.header("💎 QFL & MIA Analysis Tool")
    with st.expander("📘 How to Use This Tool", expanded=False):
        st.markdown("""This tool analyzes sandstone composition to determine provenance and weathering intensity.
        1.  **Enter API Key**: Add your OpenAI API key in the sidebar.
        2.  **Provide Data**: Upload a CSV file or enter data manually in the table.
        3.  **Process Data**: Click the "Process Data" button to run the analysis.
        4.  **Generate AI Report**: Go to the AI tab to generate a detailed geological report and ask follow-up questions.""")

    with st.form("data_input_form"):
        st.subheader("1. Data Input")
        input_type = st.radio("Choose Input Type:", ["🔬 Full Mineral Data", "📊 Direct Q-F-L Values"], horizontal=True)
        df_input = None
        if input_type == "🔬 Full Mineral Data":
            sample_data = pd.DataFrame([{'Sample': 'S1', 'Qm': 48.4, 'Qp': 7.8, 'K': 7.8, 'P': 5.4, 'Lm': 7.6, 'Ls': 8.0, 'Lv': 0.0}, {'Sample': 'S2', 'Qm': 10.0, 'Qp': 5.0, 'K': 40.0, 'P': 5.0, 'Lm': 15.0, 'Ls': 10.0, 'Lv': 15.0}])
            st.markdown("###### Enter Full Mineral Data or Upload CSV")
        else:
            sample_data = pd.DataFrame([{'Sample': 'S1', 'Q': 60.0, 'F': 15.0, 'L': 25.0}, {'Sample': 'S2', 'Q': 20.0, 'F': 50.0, 'L': 30.0}])
            st.markdown("###### Enter Direct Q-F-L Values or Upload CSV")
        col1, col2 = st.columns([2, 1])
        with col1:
            df_input = st.data_editor(sample_data, num_rows="dynamic", use_container_width=True)
        with col2:
            uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
            if uploaded_file:
                df_input = pd.read_csv(uploaded_file)
        submitted = st.form_submit_button("🚀 Process Data")

    if submitted:
        df = df_input.copy()
        df.columns = [c.strip().lower() for c in df.columns]
        try:
            if input_type == "🔬 Full Mineral Data":
                rename_map = {"feldspar": "k", "mica": "p", "lithic fragment": "lv"}
                df = df.rename(columns=rename_map)
                expected_cols = ["qm", "qp", "k", "p", "lm", "ls", "lv"]
                if not all(col in df.columns for col in expected_cols):
                    st.error(f"Missing required columns: {', '.join([c for c in expected_cols if c not in df.columns])}")
                    return
                for col in expected_cols: df[col] = pd.to_numeric(df[col], errors='coerce')
                df = df.dropna(subset=expected_cols)
                df["Q"] = df["qm"] + df["qp"]
                df["F"] = df["k"] + df["p"]
                df["L"] = df["lm"] + df["ls"] + df["lv"]
            else:
                expected_cols = ["q", "f", "l"]
                if not all(col in df.columns for col in expected_cols):
                    st.error(f"Missing required columns: {', '.join([c for c in expected_cols if c not in df.columns])}")
                    return
                for col in expected_cols: df[col] = pd.to_numeric(df[col], errors='coerce')
                df = df.dropna(subset=expected_cols)
            qfl_sum = df[['Q', 'F', 'L']].sum(axis=1)
            df['Q_norm'] = df['Q'] / qfl_sum
            df['F_norm'] = df['F'] / qfl_sum
            df['L_norm'] = df['L'] / qfl_sum
            df['MIA'] = (df['Q'] / (df['Q'] + df['F'])).multiply(100).fillna(0)
            st.session_state.processed_data = df
            st.session_state.ai_report = None
            st.session_state.ai_answer = None
            st.success("✅ Data processed successfully! View results below.")
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
            st.session_state.processed_data = None

    if st.session_state.processed_data is not None:
        df_processed = st.session_state.processed_data
        st.subheader("2. Analysis Results")
        tab_titles = ["📊 Results Table", "📈 QFL Plot", "🔬 MIA Analysis", "🤖 AI Interpretation", "📥 Download"]
        tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_titles)
        with tab1:
            st.markdown("#### Processed Data Table")
            display_cols = ['Q', 'F', 'L', 'MIA'] + [c for c in ['qm', 'qp', 'k', 'p', 'lm', 'ls', 'lv'] if c in df_processed.columns]
            st.dataframe(df_processed.style.format({col: "{:.2f}" for col in display_cols}), use_container_width=True)
            st.metric(label="Average Maturity Index (MIA)", value=f"{df_processed['MIA'].mean():.2f}%")
        with tab2:
            st.markdown("#### Interactive QFL Provenance Plot")
            st.plotly_chart(create_qfl_mia_plot(df_processed), use_container_width=True)
        with tab3:
            st.markdown("#### Maturity Index (MIA) by Sample")
            mia_fig = px.bar(df_processed, y='MIA', title="Maturity Index of Arenites (MIA)", labels={'index': 'Sample', 'MIA': 'MIA (%)'}, text=df_processed['MIA'].apply(lambda x: f'{x:.1f}%'))
            mia_fig.update_layout(yaxis_range=[0,100])
            st.plotly_chart(mia_fig, use_container_width=True)
            st.info("""**MIA Interpretation:** High MIA (>75%) suggests intense weathering (stable/humid), while Low MIA (<75%) suggests less weathering (active/arid).""")
        with tab4:
            st.markdown("#### AI-Powered Geological Analysis")
            st.warning("Ensure your OpenAI API key is entered in the sidebar to use this feature.")
            
            if st.button("Generate Geological Report", key="gen_report"):
                api_key = st.session_state.get("openai_api_key")
                if not api_key:
                    st.error("Please enter your OpenAI API key in the sidebar first.")
                else:
                    with st.spinner("👩‍🔬 The AI geologist is analyzing your data... this may take a moment."):
                        report = get_ai_interpretation(api_key, df_processed)
                        st.session_state.ai_report = report
            
            if st.session_state.ai_report:
                st.markdown("---")
                st.markdown(st.session_state.ai_report)
                
                st.markdown("---")
                st.subheader("Ask a Follow-up Question")
                user_question = st.text_area("Enter your question about the report:", key="ai_question")
                if st.button("Get Answer", key="get_answer"):
                    api_key = st.session_state.get("openai_api_key")
                    if not user_question:
                        st.error("Please enter a question.")
                    elif not api_key:
                        st.error("Please enter your OpenAI API key in the sidebar.")
                    else:
                        with st.spinner("Thinking..."):
                            answer = get_ai_answer(api_key, st.session_state.ai_report, user_question)
                            st.session_state.ai_answer = answer

                if st.session_state.ai_answer:
                    st.info(st.session_state.ai_answer)

        with tab5:
            st.markdown("#### Download Center")
            csv = df_processed.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download Results as CSV", data=csv, file_name="geolab_pro_results.csv", mime="text/csv", use_container_width=True)
            
            if st.session_state.ai_report:
                st.download_button(
                    label="📥 Download Report as Text File",
                    data=st.session_state.ai_report,
                    file_name="ai_geological_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# --- Other UI Modules (unchanged) ---
def stereonet_plotter_ui():
    st.header("🧭 Stereonet Plotter")
    st.markdown("Visualize planes and lines on an equal-area (Schmidt) lower-hemisphere stereonet.")
    with st.form("stereonet_form"):
        st.subheader("Plane"); col1, col2 = st.columns(2)
        with col1: strike = st.number_input("Strike of Plane (°)", 0.0, 360.0, 30.0)
        with col2: dip = st.number_input("Dip of Plane (°)", 0.0, 90.0, 45.0)
        st.subheader("Lineation"); col3, col4 = st.columns(2)
        with col3: trend = st.number_input("Trend of Line (°)", 0.0, 360.0, 150.0)
        with col4: plunge = st.number_input("Plunge of Line (°)", 0.0, 90.0, 25.0)
        if st.form_submit_button("🔍 Plot Stereonet"):
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
            ax.set_theta_zero_location('N'); ax.set_theta_direction(-1); ax.set_rlim(0, 1); ax.set_yticklabels([]); ax.grid(True); ax.set_title("Lower-Hemisphere Equal-Area Stereonet", pad=20)
            strike_rad, dip_rad = np.deg2rad(strike), np.deg2rad(dip); dip_direction_rad = strike_rad + np.pi / 2; alpha = np.linspace(-np.pi/2, np.pi/2, 100)
            trend_great_circle = dip_direction_rad + np.arctan(np.tan(alpha) / np.cos(dip_rad)); plunge_great_circle = np.arcsin(np.sin(alpha) * np.sin(dip_rad))
            r_plane = np.sqrt(2) * np.sin(np.pi/4 - plunge_great_circle/2); ax.plot(trend_great_circle, r_plane, label=f'Plane ({strike:.0f}/{dip:.0f})', color='b')
            trend_rad, plunge_rad = np.deg2rad(trend), np.deg2rad(plunge); r_line = np.sqrt(2) * np.sin(np.pi/4 - plunge_rad/2); ax.plot(trend_rad, r_line, 'ro', markersize=8, label=f'Line ({trend:.0f}/{plunge:.0f})')
            ax.legend(); st.pyplot(fig); create_download_button(fig, "stereonet_plot.png")

def true_dip_calculator_ui():
    st.header("📐 True Dip from Apparent Dips"); st.markdown("Calculate the true dip of a plane from an apparent dip measurement.")
    with st.form("truedip_form"):
        apparent_dip = st.number_input("Apparent Dip (°)", 0.0, 90.0, 30.0); angle_diff = st.number_input("Angle Between Strike and Traverse (°)", 0.1, 90.0, 45.0)
        if st.form_submit_button("🔍 Calculate True Dip"):
            true_dip = math.degrees(math.atan(math.tan(math.radians(apparent_dip)) / math.sin(math.radians(angle_diff))))
            st.success(f"**Calculated True Dip: {true_dip:.2f}°**"); st.latex(r"\text{True Dip} = \arctan\left(\frac{\tan(\text{Apparent Dip})}{\sin(\text{Angle Difference})}\right)")

def porosity_calculator_ui():
    st.header("🪨 Rock Porosity Calculator"); st.markdown("Calculate porosity from pore volume and total bulk volume.")
    with st.form("porosity_form"):
        pore_volume = st.number_input("Pore Volume (e.g., cm³)", 0.0, value=25.0); total_volume = st.number_input("Total Bulk Volume (e.g., cm³)", 0.0, value=100.0)
        if st.form_submit_button("🔍 Calculate Porosity"):
            if total_volume <= 0: st.error("Total Bulk Volume must be > 0.")
            else: porosity = (pore_volume / total_volume) * 100; st.success(f"**Calculated Porosity: {porosity:.2f}%**"); st.latex(r"\text{Porosity (\%)} = \left(\frac{\text{Pore Volume}}{\text{Total Volume}}\right) \times 100")

def strat_thickness_ui():
    st.header("📏 Stratigraphic Thickness Estimator"); st.markdown("Calculate true thickness from measured thickness and dip angle.")
    with st.form("thickness_form"):
        measured_thickness = st.number_input("Measured Thickness (units)", 0.0, value=50.0); dip_angle = st.number_input("Dip Angle (°)", 0.0, 90.0, value=30.0)
        if st.form_submit_button("🔍 Calculate True Thickness"):
            true_thickness = measured_thickness * math.sin(math.radians(dip_angle)); st.success(f"**True Stratigraphic Thickness: {true_thickness:.2f} units**"); st.latex(r"\text{True Thickness} = \text{Measured Thickness} \times \sin(\text{Dip Angle})")

def slope_gradient_ui():
    st.header("⛰️ Slope Gradient Calculator"); st.markdown("Calculate slope gradient from vertical rise and horizontal run.")
    with st.form("slope_form"):
        rise = st.number_input("Vertical Rise (units)", 0.0, value=10.0); run = st.number_input("Horizontal Run (units)", 0.0, value=100.0)
        if st.form_submit_button("🔍 Calculate Slope Gradient"):
            if run <= 0: st.error("Horizontal Run must be > 0.")
            else: slope = (rise / run) * 100; st.success(f"**Slope Gradient: {slope:.2f}%**"); st.latex(r"\text{Slope Gradient (\%)} = \left(\frac{\text{Vertical Rise}}{\text{Horizontal Run}}\right) \times 100")

def grain_size_to_phi_ui():
    st.header("🌾 Grain Size (mm) to Phi (φ) Converter"); st.markdown("Convert grain size from millimeters to the logarithmic Phi (φ) scale.")
    with st.form("phi_form"):
        grain_size_mm = st.number_input("Grain Size (mm)", 0.0001, value=1.0, format="%.4f")
        if st.form_submit_button("🔍 Calculate Phi (φ)"):
            phi_value = -math.log2(grain_size_mm); st.success(f"**Phi (φ) Value: {phi_value:.2f} φ**"); st.latex(r"\phi = -\log_2(\text{Grain Size in mm})")

# --- NAVIGATION & MAIN APP LAYOUT ---
def display_homepage():
    st.markdown("""<style>.home-title{font-size:3.5rem;font-weight:700;color:#1E90FF;text-align:center}.home-subtitle{font-size:1.5rem;color:#4F4F4F;text-align:center;margin-bottom:2rem}.feature-list{font-size:1.1rem;margin-top:1rem;list-style-position:inside;text-align:left}</style>""", unsafe_allow_html=True)
    lottie_earth_logo = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_iv4dsx3q.json")
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        if lottie_earth_logo: st_lottie(lottie_earth_logo, height=350, speed=1, loop=True)
    with col2:
        st.markdown('<h1 class="home-title">Welcome to GeoLab Pro</h1>', unsafe_allow_html=True); st.markdown('<p class="home-subtitle">Your Professional Toolkit for Geoscience</p>', unsafe_allow_html=True)
        st.markdown("""**GeoLab Pro** is designed for geology students and professionals, offering a suite of powerful tools for geological calculations and visualizations.<ul class="feature-list"><li>✔️ Instant and accurate calculations.</li><li>✔️ Interactive and downloadable plots.</li><li>✔️ User-friendly interface for students & researchers.</li></ul><br>Select a module from the sidebar to begin your analysis.""", unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    st.sidebar.title("GeoLab Pro")
    st.sidebar.header("AI Configuration")
    # WARNING: Do not expose your API key publicly. Use st.secrets for deployment.
    st.session_state.openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value="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")
    st.sidebar.markdown("---")

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.selected_module = None
        st.session_state.processed_data = None
        st.session_state.ai_report = None
        st.session_state.ai_answer = None
        st.rerun()
    st.sidebar.subheader("Analysis Modules")
    for display_name, mod_id in MODULES.items():
        if st.sidebar.button(display_name, use_container_width=True):
            st.session_state.selected_module = mod_id
            st.rerun()
    if st.session_state.selected_module is None:
        display_homepage()
    else:
        ui_function_map = {"qfl_mia_tool": qfl_mia_tool_ui, "stereonet_plotter": stereonet_plotter_ui, "true_dip_calculator": true_dip_calculator_ui, "porosity_calculator": porosity_calculator_ui, "strat_thickness_estimator": strat_thickness_ui, "slope_gradient": slope_gradient_ui, "grain_size_to_phi": grain_size_to_phi_ui}
        selected_function = ui_function_map.get(st.session_state.selected_module)
        if selected_function: selected_function()
    st.markdown("---"); st.markdown("""<div style="text-align:center; font-size:12px; color:gray; padding:10px;">Developed with ❤️ by <b>Anindo Paul Sourav</b><br>Department of Geology and Mining, University of Barishal</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
