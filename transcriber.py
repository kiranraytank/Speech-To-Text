import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv()
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")

def transcribe_short_audio(audio_path):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_input = speechsdk.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = recognizer.recognize_once()
    return result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else "No speech recognized."

def transcribe_full_audio(audio_path):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_input = speechsdk.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    full_transcript = []

    def handle_result(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            full_transcript.append(evt.result.text)

    recognizer.recognized.connect(handle_result)
    recognizer.start_continuous_recognition()
    import time; time.sleep(30)  # Adjust based on audio length
    recognizer.stop_continuous_recognition()

    return " ".join(full_transcript)
