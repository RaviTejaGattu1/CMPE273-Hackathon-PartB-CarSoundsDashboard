import pika

def send_to_queue(file_path):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="audio_queue")
    channel.basic_publish(exchange="", routing_key="audio_queue", body=file_path.encode())
    connection.close()
    print(f"Sent {file_path} to queue")

if __name__ == "__main__":
    send_to_queue("dataset/fan/section_00_source_train_normal_0052_strength_1_ambient.wav")