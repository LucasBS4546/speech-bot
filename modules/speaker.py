from loguru import logger
from gtts import gTTS
import pygame
import time
import os


class Speaker:
    def __init__(self, audio_dir: str, language: str = "en"):
        self.audio_dir = audio_dir
        self.language = language
        self.counter = 0

    def speak(self, message: str):
        if not message:
            return

        if "-" in self.language:
            self.language = self.language.split("-")[0].strip()

        audio_obj = gTTS(text=message, lang=self.language, slow=False)

        file_path = os.path.join(self.audio_dir, f"audio{self.counter}.mp3")
        audio_obj.save(file_path)

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.counter += 1

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        try:
            os.remove(file_path)
            self.counter -= 1
        except Exception as e:
            logger.warning(f"Failed deleting audio file {file_path}: {e}")
