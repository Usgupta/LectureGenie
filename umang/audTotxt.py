import openai
import requests
import json
import base64

# Set up your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Set up the API endpoint URL
api_url = "https://api.openai.com/v1/speech-to-text"

# Specify the audio file you want to transcribe
audio_file = "path/to/your/audio_file.wav"

# Read the audio file data
with open(audio_file, "rb") as f:
    audio_data = f.read()

# Encode the audio data as base64
audio_base64 = base64.b64encode(audio_data).decode()

# Set up the request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}",
}

# Set up the request data
data = {
    "model": "ada",
    "audio": audio_base64,
}

# Make the API request
response = requests.post(api_url, headers=headers, json=data)

# Parse the response data
response_data = json.loads(response.text)

# Print the transcribed text
transcript = response_data["text"]
print(transcript)
