import streamlit as st
from video_processor import VideoProcessor
from transcription_service import TranscriptionService
from text_improvement_service import TextImprovementService
from tts_service import TTSService
from audio_replacement_service import AudioReplacementService

class App:
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.transcription_service = TranscriptionService()
        self.text_improvement_service = TextImprovementService()
        self.tts_service = TTSService()
        self.audio_replacement_service = AudioReplacementService()

    def run(self):
        st.title("Video Audio Replacement PoC")

        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

        if uploaded_file is not None:
            st.video(uploaded_file)

            if st.button("Process Video"):
                with st.spinner("Processing video..."):
                    try:
                        # Extract audio from video
                        audio_file = self.video_processor.extract_audio(uploaded_file)

                        # Transcribe audio
                        words_with_timestamps = self.transcription_service.transcribe(audio_file)
                        st.write("Original Transcription:", " ".join([word["word"] for word in words_with_timestamps]))

                        # Improve transcription
                        improved_words_with_timestamps = self.text_improvement_service.improve(words_with_timestamps)
                        st.write("Improved Transcription:", " ".join([word["word"] for word in improved_words_with_timestamps]))

                        # Generate new audio
                        new_audio = self.tts_service.synthesize(improved_words_with_timestamps)

                        # Replace audio in video
                        uploaded_file.seek(0)
                        final_video = self.audio_replacement_service.replace_audio(uploaded_file, new_audio)

                        st.success("Video processing complete!")
                        st.video(final_video)
                    except Exception as e:
                        st.error(f"An error occurred during processing: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.run()
