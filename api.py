from fastapi import FastAPI, UploadFile
from model import predict_sound
import os

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile):
    # Save uploaded file temporarily
    temp_path = f"uploads/temp_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    # Run prediction
    result = predict_sound(temp_path)
    # Clean up
    os.remove(temp_path)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
