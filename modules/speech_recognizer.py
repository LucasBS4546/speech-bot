import speech_recognition as sr
from loguru import logger


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def calibrate(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def recognize_audio(self, language: str = "en-US") -> str | None:
        try:
            logger.debug("Listening for speech...")

            with self.mic as source:
                audio = self.recognizer.listen(source, phrase_time_limit=10)

                return self.recognizer.recognize_google(
                    audio, language=language
                ).lower()

        except sr.UnknownValueError:
            logger.warning("Could not understand audio")

        except sr.RequestError as e:
            logger.error(f"API Error: {e}")

        return None

    def close_recognizer(self) -> None:
        if hasattr(self.mic, "stream") and self.mic.stream:
            self.mic.stream.close()
