import speech_recognition as sr
import os
from logger.logger import Logger
logger = Logger.get_logger()




def convert_audio_file_to_text(audio_path):
    """ convert audio file to text. receives path of audio file and return the transcribed text.
        using with recognize_sphinx. in case of Error return None """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"No such file or directory: {audio_path}")
    audio = sr.AudioData.from_file(audio_path)
    r = sr.Recognizer()
    try:
        transcribed_text = r.recognize_sphinx(audio)
        print(f"Sphinx thinks you said: {transcribed_text}")
        return transcribed_text
    except sr.UnknownValueError:
        logger.error("Sphinx could not understand audio")
    except sr.RequestError as e:
        logger.error(f"Sphinx error: {e}")


if __name__ == "__main__":
    convert_audio_file_to_text("C:\\python_data\\podcasts\\download (6).wav")