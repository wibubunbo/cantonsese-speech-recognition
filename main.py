from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
import librosa
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import io

# Initialize the model and processor
MODEL_NAME = "alvanlii/whisper-small-cantonese"
processor = WhisperProcessor.from_pretrained(MODEL_NAME)
model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)

model.config.forced_decoder_ids = None
model.config.suppress_tokens = []
model.config.use_cache = False

app = FastAPI()

@app.post("/speech_to_text")
async def speech_to_text(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.mp3'):
        raise HTTPException(status_code=400, detail="Only MP3 files are allowed")
    # Read the uploaded file
    contents = await file.read()
    audio_data = io.BytesIO(contents)

    # Load the audio file
    y, sr = librosa.load(audio_data, sr=16000)

    # Process the audio
    processed_in = processor(y, sampling_rate=sr, return_tensors="pt")
    gout = model.generate(
        input_features=processed_in.input_features, 
        output_scores=True, return_dict_in_generate=True
    )
    
    # Get the transcription
    transcription = processor.batch_decode(gout.sequences, skip_special_tokens=True)[0]

    return {"transcription": transcription}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Speech-to-Text API"}