from pyAudioAnalysis import audioTrainTest as aT
import numpy as np

def predict_sound(file_path):
    # Classify using the trained model (now in HACKATHON root)
    model_path = "motorsoundsmodel"  # No need for dataset/ prefix since it's in the root
    c, probabilities, class_names = aT.file_classification(file_path, model_path, "gradientboosting")
    
    # Get predicted class and confidence
    max_index = np.argmax(probabilities)
    predicted_class = class_names[max_index]
    confidence = probabilities[max_index]
    
    # Determine status (confidence < 0.7 indicates an issue, adjust as needed)
    status = "normal" if confidence >= 0.7 else "issue"
    
    return {
        "sound": predicted_class,
        "status": status,
        "confidence": round(float(confidence), 5)  # Convert to native float for JSON
    }

if __name__ == "__main__":
    # Test with a sample file
    result = predict_sound("dataset/fan/section_00_source_train_normal_0050_strength_1_ambient.wav")
    print(result)