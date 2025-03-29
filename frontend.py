import streamlit as st
from producer import send_to_queue
import requests
import os
import json
import time

# Set page configuration for a wider layout and sci-fi theme
st.set_page_config(page_title="Vehicle State Approval", layout="wide")

# Custom CSS for sci-fi theme with gradient background and animations
st.markdown(
    """
    <style>
    /* Gradient background for the entire page */
    .stApp {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #415a77 100%);
        color: #e0e1dd;
        font-family: 'Orbitron', sans-serif;
    }

    /* Title styling with glowing effect */
    h1 {
        color: #00ffcc;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 30px #00ffcc;
        text-align: center;
        animation: glow 2s ease-in-out infinite alternate;
    }

    /* Subheader styling */
    h3 {
        color: #778da9;
        text-align: center;
    }

    /* File uploader styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid #00ffcc;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
    }

    /* Result container styling */
    .result-container {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #00ffcc;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    /* Icon styling */
    .icon {
        vertical-align: middle;
        margin-right: 10px;
    }

    /* Status text styling */
    .status-normal {
        color: #00ff00;
        text-shadow: 0 0 5px #00ff00;
    }
    .status-issue {
        color: #ff3333;
        text-shadow: 0 0 5px #ff3333;
    }

    /* Loading animation container */
    .loader-container {
        position: relative;
        width: 200px;
        height: 100px;
        margin: 20px auto;
        text-align: center;
    }

    /* Car icon styling */
    .car-icon {
        width: 150px;
        position: absolute;
        bottom: 0;
        left: 25px;
    }

    /* Magnifying glass icon styling */
    .magnifying-glass {
        width: 50px;
        position: absolute;
        bottom: 30px;
        left: 0;
        animation: scan 2s linear infinite;
    }

    /* Animation for magnifying glass */
    @keyframes scan {
        0% { left: 0; }
        50% { left: 150px; }
        100% { left: 0; }
    }

    /* Keyframes for glowing effect */
    @keyframes glow {
        from {
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 30px #00ffcc;
        }
        to {
            text-shadow: 0 0 20px #00ffcc, 0 0 30px #00ffcc, 0 0 40px #00ffcc;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load a sci-fi font (Orbitron) from Google Fonts
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Header with sci-fi banner (using Imgur URL, resized)
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <img src="https://i.imgur.com/6R7RGQl.jpeg" style="width: 10%; border-radius: 10px; box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);">
    </div>
    """,
    unsafe_allow_html=True
)
st.title("Vehicle State Approval")
st.markdown("### Upload motor sounds to analyze vehicle status (supports multiple files).")

# Initialize session state for results and file uploader key
if 'results' not in st.session_state:
    st.session_state.results = []
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

# File uploader (allow multiple files)
uploaded_files = st.file_uploader(
    "Choose audio files",
    type=["wav"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
)

# Process uploaded files
if uploaded_files:
    # Show loading animation
    loading_placeholder = st.empty()
    loading_placeholder.markdown(
        """
        <div class="loader-container">
            <img src="https://img.icons8.com/fluency/48/000000/car.png" class="car-icon" alt="Car Icon">
            <img src="https://img.icons8.com/fluency/48/000000/search.png" class="magnifying-glass" alt="Magnifying Glass">
        </div>
        <p style="text-align: center; color: #00ffcc;">Processing files...</p>
        """,
        unsafe_allow_html=True
    )

    # Save files locally, send to queue, and get immediate results
    os.makedirs("uploads", exist_ok=True)
    new_results = []
    for uploaded_file in uploaded_files:
        file_path = f"uploads/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Send to queue for background logging
        send_to_queue(file_path)

        # Direct API call for immediate feedback
        with open(file_path, "rb") as f:
            response = requests.post("http://localhost:8000/predict", files={"file": f})
        result = response.json()
        result["file"] = file_path
        new_results.append(result)

    # Clear loading animation
    loading_placeholder.empty()

    # Add new results to session state
    st.session_state.results.extend(new_results)

    # Clear the file uploader by incrementing the key
    st.session_state.uploader_key += 1
    st.rerun()  # Use st.rerun() for Streamlit 1.40.1

# Function to load results from results.json (for queue updates)
def load_results():
    results_file = "results.json"
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Function to clear results
def clear_results():
    with open("results.json", "w") as f:
        json.dump([], f)
    st.session_state.results = []

# Buttons for manual refresh and clear
col1, col2 = st.columns(2)
with col1:
    if st.button("Refresh Results (from queue)"):
        st.session_state.results = load_results()
        st.rerun()
with col2:
    if st.button("Clear Results"):
        clear_results()
        st.rerun()

# Display processed results
if st.session_state.results:
    st.markdown("### Processed Results")
    for result in st.session_state.results:
        color_class = "status-normal" if result["status"] == "normal" else "status-issue"
        st.markdown(
            f"""
            <div class="result-container">
                <div>
                    <img src="https://img.icons8.com/fluency/48/000000/audio-wave.png" class="icon" alt="Sound Icon">
                    <span style="color: #00ffcc;">File:</span> {result['file']}
                </div>
                <div>
                    <img src="https://img.icons8.com/fluency/48/000000/audio-wave.png" class="icon" alt="Sound Icon">
                    <span style="color: #00ffcc;">Sound:</span> {result['sound']}
                </div>
                <div>
                    <img src="https://img.icons8.com/fluency/48/000000/traffic-light.png" class="icon" alt="Status Icon">
                    <span style="color: #00ffcc;">Status:</span> <span class="{color_class}">{result['status']}</span>
                </div>
                <div>
                    <img src="https://img.icons8.com/fluency/48/000000/speed.png" class="icon" alt="Confidence Icon">
                    <span style="color: #00ffcc;">Confidence:</span> {result['confidence']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )