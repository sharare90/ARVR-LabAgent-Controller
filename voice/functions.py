import os

import playsound
from voice.config import texts
from google.cloud import texttospeech


def say_text_by_id(text_id):
    file_path = f'voice/recordings/{text_id}.mp3'
    if not os.path.exists(file_path):
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.types.SynthesisInput(text=texts[text_id])
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        with open(file_path, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
    print('\n\n\n\n\n')
    print(file_path)
    print('\n\n\n\n\n')
    playsound.playsound(file_path, True)

global counter
counter = 2

def say_text(text):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    global counter
    counter += 1
    with open(f'output{counter}.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)

    playsound.playsound(f'output{counter}.mp3', True)