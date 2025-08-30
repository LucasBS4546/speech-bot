from loguru import logger
from playwright.sync_api import Page

from modules.speaker import Speaker
from modules.speech_recognizer import SpeechRecognizer

from utils.exceptions import SpeechInterrupt

from tasks.time_information import hour_info, day_info


class CommandInterpreter:
    def __init__(
        self,
        recognizer: SpeechRecognizer,
        speaker: Speaker,
        page: Page,
        language: str,
        hotword: str,
    ):
        self.recognizer = recognizer
        self.speaker = speaker
        self.page = page
        self.hotword = hotword.lower()
        self.language = None

        self._set_language(language=language)

    def _set_language(self, language: str) -> None:
        logger.info(
            f"Language changed: {self.language} -> {language}"
            if self.language
            else f"Language set to {language}"
        )
        self.language = language
        self.speaker.language = language

    def read_command(self, user_input: str) -> str | None:
        has_hotword, text = self._detect_hotword(user_input)

        if not has_hotword:
            logger.debug(
                f"Hotword '{self.hotword}' not detected. Ignoring input: '{text}'"
            )
            return None

        logger.debug(f"text received: {text}")
        command = text.split(self.hotword, 1)[1].strip()

        if not command:
            logger.debug("No command detected after hotword.")
            command = None
        else:
            logger.debug(f"Command received: '{command}'")

        if self.language == "pt-BR":
            return self._pt_commands(command=command)

        elif self.language == "en-US":
            return self._en_commands(command=command)

        else:
            return self._en_commands(command=command)

    def _detect_hotword(self, text: str) -> tuple:
        if self.language == "pt-BR":
            if text.startswith("alexia"):
                text = "alexa" + text[6:]

        return text.startswith(self.hotword), text

    def _en_commands(self, command: str | None) -> str:
        if command is None:
            return "I couldn't understand the command, could you say it again?"

        elif command == "hello":
            return "hello world"

        elif command.startswith("say "):
            return command.split("say")[1]

        elif command in ["change language to portuguese", "portuguese"]:
            self._set_language("pt-BR")
            return "Idioma alterado para português"

        elif command in ["what time is it", "what time is it?", "time", "current time"]:
            h, m, s = hour_info("hour", "minute", "second")
            return f"{h} {m} and {s}"

        elif command in ["what day is it", "what day is it?"]:
            weekday, day, month, year = day_info("en")
            return f"{weekday}, {day} of {month} of {year}"

        elif command in ["stop listening", "shut down", "shutdown"]:
            raise SpeechInterrupt("shutting down")

        else:
            return "I couldn't understand the command, could you say it again?"

    def _pt_commands(self, command: str | None) -> str:
        if command is None:
            return "Não entendi seu comando, pode repetir?"

        elif command in ["ola", "olá"]:
            return "olá mundo"

        elif command.startswith("diga "):
            return command.split("diga")[1]

        elif command in ["mudar idioma para inglês", "inglês"]:
            self._set_language("en-US")
            return "Language set to english"

        elif command in ["que horas são", "que horas são?", "horário", "horas"]:
            h, m, s = hour_info("hora", "minuto", "segundo")
            return f"{h} {m} e {s}"

        elif command in ["que dia é hoje", "que dia é hoje?"]:
            weekday, day, month, year = day_info("pt")
            return f"{weekday}, dia {day} de {month} de {year}"

        elif command == "desligar":
            raise SpeechInterrupt("desligando")

        else:
            return "Não entendi seu comando, pode repetir?"
