from google import genai
from google.genai import types
import wave


def voice_gen(text, voice_name='Kore', file_name='out.wav'):
   
    # Set up the wave file to save the output:
    def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)

    client = genai.Client(api_key = "AIzaSyBQ6lbuVpoRH7ttKndxTb__YmcjrTVWJ3s")

    response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=text,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Kore',
                )
            )
        ),
    )
    )

    data = response.candidates[0].content.parts[0].inline_data.data
    print(f"Audio content written to file: {file_name}")

    wave_file(file_name, data) 