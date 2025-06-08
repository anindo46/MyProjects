import streamlit as st
import openai

# Securely load your OpenAI key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["openai_key"])

st.title("🌍 GeoSmart Tutor - AI Powered")

location = st.text_input("Enter a district or upazila name:")
language = st.selectbox("Select language:", ["English", "Bengali"])

if location:
    with st.spinner("Fetching geological data..."):
        prompt = (
            f"What is the geological formation, age, lithology, rock types, soil type, "
            f"hydrogeological setting, and environmental hazards of {location}, Bangladesh? "
        )
        if language == "Bengali":
            prompt += "Translate the full answer into Bengali."

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if enabled
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Failed to fetch response:\n\n{e}")
else:
    st.info("ℹ️ Enter a location to get started.")
