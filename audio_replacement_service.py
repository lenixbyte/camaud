from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import tempfile
import os

class AudioReplacementService:
    def replace_audio(self, video_file, audio_file):
        # Create a temporary file for the video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            temp_video_path = temp_video.name

        # Load the video
        video = VideoFileClip(temp_video_path)
        
        # Load the new audio
        new_audio = AudioSegment.from_file(audio_file, format="aiff")
        
        # Convert AudioSegment to AudioFileClip
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            new_audio.export(temp_audio.name, format='wav')
            new_audio_clip = AudioFileClip(temp_audio.name)
        
        # Set the duration of the new audio to match the video
        new_audio_clip = new_audio_clip.set_duration(video.duration)
        
        # Set the new audio to the video
        final_video = video.set_audio(new_audio_clip)
        
        # Write the result to a file
        output_file = "output_video.mp4"
        final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        
        # Close the clips and remove temporary files
        video.close()
        new_audio_clip.close()
        os.remove(temp_video_path)
        os.remove(temp_audio.name)
        
        return output_file
