import streamlit as st
import openai

# Use your API key securely from Streamlit secrets
openai.api_key = st.secrets["openai_key"]

st.title("🌍 GeoSmart Tutor - AI Powered")

location = st.text_input("Enter a district or upazila name:")
language = st.selectbox("Select language:", ["English", "Bengali"])

if location:
    with st.spinner("Fetching geological data..."):
        prompt = f"What is the geological formation, age, lithology, rock types, soil type, hydrogeological setting, and environmental hazards of {location}, Bangladesh? Provide a structured answer."
        if language == "Bengali":
            prompt += " Translate the answer into Bengali."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ Failed to fetch response: {e}")
else:
    st.info("ℹ️ Enter a location to get started.")
