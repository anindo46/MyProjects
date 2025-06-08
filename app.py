
import streamlit as st
import requests

# ✅ Use a stable, public Hugging Face model
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": f"Bearer {st.secrets['hf_api_key']}"}

st.title("ðﾟﾌﾍ GeoSmart Tutor - Hugging Face (100% Free)")

# User input
location = st.text_input("Enter a district or upazila in Bangladesh:")
language = st.selectbox("Select Language", ["English", "Bengali"])

if location:
    with st.spinner("Generating geology information..."):
        # Instruction prompt for the AI model
        prompt = (
            f"What is the geological formation, lithology, rock types, soil type, "
            f"hydrogeological setting, and environmental hazards of {location}, Bangladesh?"
        )
        if language == "Bengali":
            prompt += " Translate the full answer into Bengali."

        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }

        try:
            # Send request to Hugging Face API
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and "generated_text" in result[0]:
                    st.markdown(result[0]['generated_text'])
                else:
                    st.error("⚠️ Unexpected response format. Try again.")
            elif response.status_code == 503:
                st.warning("ðﾟﾕﾒ Model is loading. Please wait and try again.")
            elif response.status_code == 401:
                st.error("❌ Unauthorized. Please check your Hugging Face API token.")
            elif response.status_code == 404:
                st.error("❌ Model not found. Please check the model name.")
            else:
                st.error(f"❌ Hugging Face API returned status {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"❌ Failed to fetch response: {e}")
else:
    st.info("ℹ️ Enter a location to get started.")
