import streamlit as st
import openai

# Make sure you have your OpenAI API key in Streamlit's secrets
openai.api_key = st.secrets["openai_key"]

st.title("🌍 GeoSmart Tutor - AI Powered")

# User input for location (district or upazila)
location = st.text_input("Enter a district or upazila name:")

# Language selection
language = st.selectbox("Select language:", ["English", "Bengali"])

# Process user input
if location:
    with st.spinner("Fetching geological data..."):
        prompt = f"Give me the geological formation, age, lithology, rock types, soil type, hydrogeological setting, and environmental hazards of {location}, Bangladesh. Provide a structured answer."
        
        # Modify prompt if user selects Bengali
        if language == "Bengali":
            prompt += " Translate the answer into Bengali."

        try:
            # OpenAI API call using the new method for v1.0+
            response = openai.Completion.create(
                model="gpt-4",  # Or use "gpt-3.5-turbo" for a smaller model
                prompt=prompt,
                max_tokens=500  # Limit response length
            )
            answer = response.choices[0].text.strip()
            st.markdown(answer)
        except Exception as e:
            st.error(f"Failed to fetch response: {e}")
else:
    st.info("Enter a location to begin.")
