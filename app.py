
import streamlit as st
import requests

# Constants
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
headers = {"Authorization": f"Bearer {st.secrets['hf_api_key']}"}

# Streamlit UI
st.title("ðﾟﾌﾍ GeoSmart Tutor - Free with Hugging Face")
location = st.text_input("Enter a district or upazila in Bangladesh:")
language = st.selectbox("Select Language", ["English", "Bengali"])

if location:
    with st.spinner("Generating geology information..."):
        # Prompt to the model
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
            result = response.json()

            if isinstance(result, list):
                st.markdown(result[0]['generated_text'])
            else:
                st.error("⚠️ Something went wrong. Try again later or check your Hugging Face token.")
        except Exception as e:
            st.error(f"❌ Failed to fetch response: {e}")
else:
    st.info("Enter a location to get started.")
