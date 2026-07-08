import streamlit as st
import requests

st.set_page_config(page_title="Shelf Scanner AI", page_icon="📚", layout="centered")

st.title("Shelf Scanner AI")
st.write("Take a picture of any bookshelf to get instant, personalized reading recommendations!")

# User input configuration section
user_pref = st.text_input(
    "What kind of books are you looking for today?", 
    placeholder="e.g., sci-fi, startup architecture, self-improvement, historical fiction"
)

# Multi-platform file processor (Supports native camera tracking on phones)
uploaded_file = st.file_uploader("Upload or snap a photo of a bookshelf", type=["jpg", "jpeg", "png"])

BACKEND_URL = "https://shelf-scanner-ai.onrender.com/api/v1/scan" # Update backend URL for production
# BACKEND_URL = "http://127.0.0.1:8000/api/v1/scan" - for local test

if uploaded_file is not None:
    # Display preview to user
    st.image(uploaded_file, caption="Target Bookshelf", use_container_width=True)
    
    if st.button("Scan Bookshelf ", type="primary"):
        if not user_pref.strip():
            st.warning("Please enter your reading preferences first!")
        else:
            with st.spinner("AI is examining the spines and curating your reading list..."):
                try:
                    # Construct multipart payload structure
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"preferences": user_pref}
                    
                    # Ship requests across the local network boundary
                    response = requests.post(BACKEND_URL, files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("status") == "success":
                            st.success(" Curated Recommendations for You:")
                            st.markdown(result["recommendations"])
                        else:
                            st.error(f"API Error: {result.get('message')}")
                    else:
                        st.error(f"Server returned an error status code: {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the Backend server. Make sure your FastAPI app is running on port 8000.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")