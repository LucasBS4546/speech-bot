import yaml


def read_yaml_file(file_path: str):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    return data


CONFIG_DATA = read_yaml_file(r"configs\configs.yaml")

AUDIO_DIR = CONFIG_DATA["AUDIO_DIR"]
LANGUAGE = CONFIG_DATA["LANGUAGE"]
HEADLESS = CONFIG_DATA["HEADLESS"]
HOTWORD = CONFIG_DATA["HOTWORD"]
