Vehicle State Approval: Car Sound Detection System 🚗🔊


💻 A real-time interactive dashboard for anomalous sound detection in machine condition monitoring, built using Python, Streamlit, and RabbitMQ, designed to analyze motor sounds from seven machine types under domain-shifted conditions.

👥 Team Members
Name	SJSU ID
Ravi Teja Gattu	017503746
Bhavika Sodagum	017506567
Vinuta Patil	018196035
Abhinav Sriharsha	017514900

<img width="1242" alt="image" src="https://github.com/user-attachments/assets/f356f212-47dd-493a-bcc3-0a30910bdf44" />


🔁 Real-Time Queue Integration
Each audio file is treated as a message in a RabbitMQ queue (audio_queue).
A producer script (producer.py) sends audio file paths to the queue for background processing.
A consumer script (consumer.py) listens to the queue, processes files via a FastAPI endpoint, and logs results to results.json.
This architecture mimics a real-world asynchronous processing pipeline, enabling the dashboard to handle batch uploads efficiently while keeping the UI responsive.
🚀 Features
📍 Component Type Analysis

Analyze sounds from seven machine types: fan, gearbox, pump, slide rail, car, train, valve.
📈 Immediate Anomaly Detection

Displays results instantly after upload, with sound type, status ("normal" or "issue"), and confidence score.
📊 Result Summary

Color-coded statuses: green for "normal," red for "issue."
Includes file path, sound type, status, and confidence for each audio file.
🎨 Sci-Fi Themed Interface

Gradient background, glowing text effects, and a custom sci-fi banner image.
Loading animation with a magnifying glass scanning over a car icon.
🔄 Background Processing (Optional)

Simulated producer-consumer setup using RabbitMQ (pika).
Results logged to results.json for historical analysis.

🧪 Tech Stack
Python 3.8
Streamlit 1.40.1
FastAPI
RabbitMQ
Docker
Requests
Pika
HTML/CSS
JSON

🏗️ Architecture Overview
Frontend (frontend.py): Streamlit-based UI with a sci-fi theme, handling file uploads, immediate API calls, and result display.
Backend API (api.py): FastAPI server with a /predict endpoint for audio file predictions.
Message Queue (RabbitMQ):
Producer (producer.py): Sends audio file paths to the audio_queue.
Consumer (consumer.py): Processes files and logs results to results.json.
Storage: Uploaded files in uploads/, queue results in results.json.
This architecture ensures scalability and responsiveness, with immediate feedback and background processing.

📊 Aspects of Output/Data
The project uses the DCASE 2021 Task 2 dataset:

Car Components: For the "car" type, sounds include engine, exhaust, and transmission noises (normal and anomalous, e.g., engine misfires).
Data Features:
10-second single-channel WAV audio clips.
Includes car sounds and environmental noise (industrial, domestic).
Training: ~1,000 normal clips per machine type (source domain), three in the target domain.
Testing: ~100 normal and anomalous clips per machine type (both domains).
Anomalies created by damaging machines (e.g., mechanical faults).
Labels: Machine type, section index, normal/anomaly status, motor speed attributes.
Output Format:
file: Path (e.g., uploads/fan_001.wav).
sound: Machine type (e.g., "fan").
status: "normal" or "issue".
confidence: Probability (e.g., 0.95).
Example: {"file": "uploads/fan_001.wav", "sound": "fan", "status": "normal", "confidence": 0.95}.
🛠️ Setup Instructions
Step 1: Activate Conda Environment
bash

Collapse

Wrap

Copy
conda create -n hackathon python=3.8
conda activate hackathon
Step 2: Install Dependencies
bash

Collapse

Wrap

Copy
pip install streamlit==1.40.1 fastapi uvicorn pika requests
Step 3: Start RabbitMQ
bash

Collapse

Wrap

Copy
docker run -d --name rabbitmq -p 5672:5672 rabbitmq
Step 4: Start the API
bash

Collapse

Wrap

Copy
cd HACKATHON
python api.py
Step 5: Start the Consumer
In a separate terminal:

bash

Collapse

Wrap

Copy
cd HACKATHON
python consumer.py
Step 6: Run the Streamlit Dashboard
In another terminal:

bash

Collapse

Wrap

Copy
cd HACKATHON
streamlit run frontend.py
Step 7: Visit the Dashboard in Your Browser
Open http://localhost:8501.

📊 Dashboard Preview
<img width="1242" alt="image" src="https://github.com/user-attachments/assets/cb201e0d-09ea-4a13-a699-ecaa4eba02ed" />


🔍 Dashboard Features
🎨 Sci-Fi Themed Interface:

Gradient background (linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #415a77 100%)).
Glowing title with Orbitron font and a custom sci-fi banner image.
📁 File Uploader:

Upload multiple WAV files at once with a prompt "Choose audio files."
⏳ Loading Animation:

Magnifying glass scanning over a car icon during processing.
📊 Result Display:

Shows file path, sound type, status ("normal" or "issue"), and confidence.
Color-coded statuses: green for "normal," red for "issue."
Includes icons for file, sound, status, and confidence.
🔄 User Controls:

"Refresh Results (from queue)": Loads queue-processed results.
"Clear Results": Resets the display and results.json.
📈 Output
<img width="1149" alt="image" src="https://github.com/user-attachments/assets/3af7c40a-e60e-4af5-bf66-ae3cc9ae8de0" />

Results are displayed immediately after upload, with the queue logging them to results.json.

Why This is the Perfect Solution
Vehicle State Approval excels in addressing the part b of cmpe273 Hackathon:
Robust Anomaly Detection: Handles domain shifts across seven machine types, including car components like engines.
Scalability: RabbitMQ ensures efficient background processing for large-scale applications.
User Experience: Immediate feedback, a sci-fi themed UI, and user controls make the app intuitive and engaging.
Real-World Applicability: Reliable anomaly detection in diverse environments for practical machine condition monitoring.
This project combines technical excellence with a polished presentation, making it a standout for the hackathon! 🚀

