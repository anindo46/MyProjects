
import streamlit as st
import openai

# Set your OpenAI API key securely in Streamlit (go to Settings > Secrets in Streamlit Cloud)
openai.api_key = st.secrets["openai_key"]

st.title("ðﾟﾌﾍ GeoSmart Tutor - AI Powered")
st.markdown("Ask for any upazila or district in Bangladesh to get geology info:")

# Input field for location
location = st.text_input("Enter a district or upazila name:")

# Language selection
language = st.selectbox("Select language:", ["English", "Bengali"])

# Generate response
if location:
    with st.spinner("Fetching geological data..."):
        prompt = f"What is the geological formation, age, lithology, rock types, soil type, hydrogeological setting, and environmental hazards of {location}, Bangladesh? Provide a structured answer."

        if language == "Bengali":
            prompt += " Translate the answer into Bengali."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
            st.markdown(answer)
        except Exception as e:
            st.error(f"Failed to fetch response: {e}")

else:
    st.info("Enter a location to begin.")
