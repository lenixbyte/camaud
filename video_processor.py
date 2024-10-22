from moviepy.editor import VideoFileClip
import tempfile
import os

class VideoProcessor:
    def extract_audio(self, video_file):
        # Create a temporary file for the video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            temp_video_path = temp_video.name

        # Extract audio from video
        video = VideoFileClip(temp_video_path)
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
        video.audio.write_audiofile(audio_file)

        # Close the video and remove the temporary video file
        video.close()
        os.remove(temp_video_path)

        return audio_file
