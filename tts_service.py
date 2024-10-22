import subprocess
import tempfile
import os

class TTSService:
    def __init__(self):
        self.rate = 200  # Words per minute

    def synthesize(self, words_with_timestamps):
        # Prepare the text with timing information
        text_with_timing = self._prepare_text_with_timing(words_with_timestamps)

        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(suffix='.aiff', delete=False) as temp_audio:
            output_file = temp_audio.name

        # Generate speech using the 'say' command
        subprocess.run(['say', '-o', output_file, '-r', str(self.rate), text_with_timing], check=True)

        return output_file

    def _prepare_text_with_timing(self, words_with_timestamps):
        text = ""
        for i, word_data in enumerate(words_with_timestamps):
            word = word_data['word']
            duration = word_data['end'] - word_data['start']
            
            # Add a pause before the word if there's a gap
            if i > 0:
                previous_word = words_with_timestamps[i - 1]
                gap = word_data['start'] - previous_word['end']
                if gap > 0.1:  # If there's a significant gap, add a pause
                    text += f"[[slnc {int(gap * 1000)}]] "
            
            # Add the word with approximate duration control
            expected_duration = (60 / self.rate) * len(word.split())
            rate_adjustment = duration / expected_duration
            text += f"[[rate {rate_adjustment:.2f}]] {word} "
        
        return text
