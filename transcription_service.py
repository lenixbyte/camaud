import speech_recognition as sr
from pydub import AudioSegment
import os
import time
import whisper
import torch

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = whisper.load_model("base")

    def transcribe(self, audio_file):
        return self.transcribe_with_timestamps(audio_file)

    def transcribe_with_timestamps(self, audio_file):
        result = self.model.transcribe(audio_file, word_timestamps=True)
        
        # Extract words with their timestamps
        words_with_timestamps = []
        for segment in result["segments"]:
            for word in segment["words"]:
                words_with_timestamps.append({
                    "word": word["word"],
                    "start": word["start"],
                    "end": word["end"]
                })
        
        return words_with_timestamps

    # Keep the fallback_transcription method as is, in case it's needed
    def fallback_transcription(self, audio_file):
        print("Using fallback transcription method...")
        sound = AudioSegment.from_wav(audio_file)
        chunk_length_ms = 30000  # 30 seconds
        chunks = [sound[i:i+chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
        
        transcript = ""
        for i, chunk in enumerate(chunks):
            chunk_file = f"temp_chunk_{i}.wav"
            chunk.export(chunk_file, format="wav")
            
            try:
                with sr.AudioFile(chunk_file) as source:
                    audio = self.recognizer.record(source)
                chunk_transcript = self.recognizer.recognize_google(audio)
                transcript += chunk_transcript + " "
            except Exception as e:
                print(f"Error transcribing chunk {i}: {e}")
            finally:
                os.remove(chunk_file)
        
        return transcript.strip()
