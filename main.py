from loguru import logger
import time
import traceback

from configs import AUDIO_DIR, LANGUAGE, HEADLESS, HOTWORD

from modules.speech_recognizer import SpeechRecognizer
from modules.speaker import Speaker
from modules.command_interpreter import CommandInterpreter


from utils.exceptions import SpeechInterrupt
from utils.file_deletion import clear_dir
from utils.webdriver import Webdriver


def main():
    logger.info("----- STARTING EXECUTION OF BOT-LBS-001-1")

    clear_dir(AUDIO_DIR)

    speech_recognizer = SpeechRecognizer()
    speaker = Speaker(audio_dir=AUDIO_DIR, language=LANGUAGE)
    webdriver = Webdriver(headless=HEADLESS)
    interpreter = CommandInterpreter(
        speech_recognizer,
        speaker,
        page=webdriver.initialize_context_page(),
        language=LANGUAGE,
        hotword=HOTWORD,
    )

    try:
        speech_recognizer.calibrate()

        while True:
            text = speech_recognizer.recognize_audio(language=interpreter.language)

            if text:
                response = interpreter.read_command(text)
                if response:
                    speaker.speak(response)

            else:
                logger.debug("No speech detected")

    except SpeechInterrupt as e:
        logger.info("Interrupted by user via speech. Exiting...")
        speaker.speak(str(e))
        time.sleep(1.5)

    except KeyboardInterrupt:
        logger.info("Interrupted by user via keyboard. Exiting...")

    except Exception:
        logger.error(f"Critical error: {traceback.format_exc()}")

    finally:
        speech_recognizer.close_recognizer()
        webdriver.quit()
        logger.info("----- END OF EXECUTION OF BOT-LBS-001-1")


if __name__ == "__main__":
    main()
