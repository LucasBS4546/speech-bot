from datetime import datetime


def get_time_data(data: str, lan: str):
    if lan == "en":
        if data == "days":
            return [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]
        if data == "months":
            return [
                "january",
                "february",
                "march",
                "april",
                "may",
                "june",
                "july",
                "august",
                "september",
                "october",
                "november",
                "december",
            ]

    if lan == "pt":
        if data == "days":
            return [
                "segunda feira",
                "terca-feira",
                "quarta feira",
                "quinta feira",
                "sexta feira",
                "sábado",
                "domingo",
            ]
        if data == "months":
            return [
                "janeiro",
                "fevereiro",
                "março",
                "abril",
                "maio",
                "junho",
                "julho",
                "agosto",
                "setembro",
                "outubro",
                "novembro",
                "dezembro",
            ]


def hour_info(h: str, m: str, s: str):
    from utils.string_formatting import pluralize

    now = datetime.now()

    return (
        f"{pluralize(now.hour, h)}",
        f"{pluralize(now.minute, m)}",
        f"{pluralize(now.second, s)}",
    )


def day_info(language: str):
    now = datetime.now()

    days = get_time_data("days", language)
    months = get_time_data("months", language)

    return days[now.weekday()], now.day, months[now.month - 1], now.year
