import streamlit as st
import streamlit.components.v1 as components
import subprocess
import time
import requests

hide_streamlit_style = """
    <style>
    /* Hide the hamburger menu */
    #MainMenu {visibility: hidden;}
    /* Hide the header */
    header {visibility: hidden;}
    /* Hide the footer */
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Define the port for Chainlit (ensure it's different from Streamlit's port)
chainlit_port = "7860"
chainlit_command = ["chainlit", "run", "app.py", "--port", chainlit_port]

# Start the Chainlit app as a subprocess
chainlit_process = subprocess.Popen(chainlit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

st.title("Streamlit App with Embedded Chainlit UI")

chainlit_url = f"http://localhost:{chainlit_port}"
timeout = 60  # Maximum wait time in seconds
start_time = time.time()

# Create a progress bar and a placeholder for status messages
progress_bar = st.progress(0)
status_text = st.empty()

with st.spinner("Waiting for Chainlit app to start..."):
    while True:
        try:
            response = requests.get(chainlit_url)
            if response.status_code == 200:
                break  # Chainlit is ready
        except Exception:
            pass  # Keep waiting if there's an error (e.g., connection refused)
        
        elapsed = time.time() - start_time
        # Update progress (capped at 100%)
        progress = min(int((elapsed / timeout) * 100), 100)
        progress_bar.progress(progress)
        status_text.text(f"Waiting... {int(elapsed)} seconds elapsed.")
        time.sleep(1)
        
        if elapsed > timeout:
            st.error("Chainlit app did not start in time.")
            st.stop()

st.success("Chainlit app loaded!")
status_text.text("")

# Embed the Chainlit app using an iframe
# components.iframe(chainlit_url, width=800)
html_code = f"""
    <style>
      .full-screen-iframe {{
         position: fixed;
         top: 0;
         left: 0;
         width: 100vw;
         height: 100vh;
         border: none;
         z-index: 9999;
      }}
    </style>
    <iframe src="{chainlit_url}" class="full-screen-iframe"></iframe>
"""

st.markdown(html_code, unsafe_allow_html=True)
