import gradio as gr
import requests
import os
from httpx import Client

http_client = Client()

CHAT_SERVICE_HOST = os.getenv("CHAT_SERVICE_HOST", "localhost")
MESSAGES_ENDPOINT = f"http://{CHAT_SERVICE_HOST}:8000/messages/"

def transcribe_audio(audio):
    if audio is None:
        return "Please upload an audio file."
    
    files = {"file": ("audio.mp3", audio)}
    try:
        response = http_client.post(MESSAGES_ENDPOINT, files=files)
        if not (200 <= response.status_code < 300):
            raise Exception(f"Failed to transcribe audio: {response.text}")
    except Exception as e:
        return f"Failed to transcribe audio: {e}"
    
    return response.text
    
iface = gr.Interface(
    fn=transcribe_audio,
    inputs=gr.Audio(sources=["microphone", "upload"], type="filepath"),
    outputs="text",
    title="Speech-to-Text Transcription",
    description="Upload an MP3 audio file or record audio to transcribe it to text."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)