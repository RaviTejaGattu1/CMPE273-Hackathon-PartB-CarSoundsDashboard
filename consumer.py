# import pika
# import requests

# def callback(ch, method, properties, body):
#     file_path = body.decode()
#     with open(file_path, "rb") as f:
#         response = requests.post("http://localhost:8000/predict", files={"file": f})
#     print(f"Processed {file_path}: {response.json()}")

# connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
# channel = connection.channel()
# channel.queue_declare(queue="audio_queue")
# channel.basic_consume(queue="audio_queue", on_message_callback=callback, auto_ack=True)
# print("Consumer started. Waiting for messages...")
# channel.start_consuming()

import pika
import requests
import json
import os

# File to store results
results_file = "results.json"

# Initialize results file if it doesn't exist
if not os.path.exists(results_file):
    with open(results_file, "w") as f:
        json.dump([], f)

def callback(ch, method, properties, body):
    file_path = body.decode()
    with open(file_path, "rb") as f:
        response = requests.post("http://localhost:8000/predict", files={"file": f})
    result = response.json()
    result["file"] = file_path
    print(f"Processed {file_path}: {result}")

    # Append result to results.json
    with open(results_file, "r") as f:
        results = json.load(f)
    results.append(result)
    with open(results_file, "w") as f:
        json.dump(results, f, indent=4)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="audio_queue")
channel.basic_consume(queue="audio_queue", on_message_callback=callback, auto_ack=True)
print("Consumer started. Waiting for messages...")
channel.start_consuming()