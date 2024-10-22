import openai
import json

class TextImprovementService:
    def __init__(self):
        openai.api_type = "azure"
        openai.api_base = "https://internshala.openai.azure.com/"
        openai.api_version = "2024-08-01-preview"
        openai.api_key = "22ec84421ec24230a3638d1b51e3a7dc"

    def improve(self, words_with_timestamps):
        # Convert the list to a JSON string for easier processing
        text_with_timing = json.dumps(words_with_timestamps)
        
        response = openai.ChatCompletion.create(
            engine="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI assistant that improves transcriptions while maintaining natural speech patterns. Preserve pauses, adjust filler words, and maintain the overall rhythm of speech."},
                {"role": "user", "content": f"Improve the following transcription, maintaining natural speech patterns and timing. The input is a JSON string of words with their start and end times. Return the improved text in the same format: {text_with_timing}"}
            ]
        )
        
        improved_text = response.choices[0].message['content']
        
        try:
            # Try to parse the improved text as JSON
            improved_data = json.loads(improved_text)
            
            # Validate the structure of the improved data
            if not isinstance(improved_data, list) or not all(isinstance(item, dict) for item in improved_data):
                raise ValueError("Improved data is not in the expected format")
            
            return improved_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Raw response: {improved_text}")
            # Return the original data if we can't parse the improved version
            return words_with_timestamps
        except ValueError as e:
            print(f"Error validating improved data: {e}")
            # Return the original data if the improved version is not in the expected format
            return words_with_timestamps
