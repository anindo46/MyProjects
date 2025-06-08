import streamlit as st
import requests

# Hugging Face API settings
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
headers = {"Authorization": f"Bearer {st.secrets['hf_api_key']}"}

# UI
st.title("🌍 GeoSmart Tutor - Hugging Face (Free)")

location = st.text_input("Enter a district or upazila in Bangladesh:")
language = st.selectbox("Select Language", ["English", "Bengali"])

if location:
    with st.spinner("Generating geology information..."):
        prompt = (
            f"What is the geological formation, lithology, rock types, soil type, "
            f"and environmental hazards of {location} in Bangladesh?"
        )
        if language == "Bengali":
            prompt += " Translate the response into Bengali."

        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)

            # 🛡️ Improved error handling
            if response.status_code != 200:
                st.error(f"❌ Hugging Face API returned status {response.status_code}")
                st.stop()

            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                st.markdown(result[0]['generated_text'])
            else:
                st.error("⚠️ Unexpected response format. Try again or check your Hugging Face key.")
        except Exception as e:
            st.error(f"❌ Failed to fetch response: {e}")
else:
    st.info("ℹ️ Enter a location to get started.")
