from enum import Enum


class SoftwareSection(Enum):
    RMK = "РМК"
    RMD = "РМД"
    terminal = "Терминал"
    exploitation = "Эксплуатация"
    timetable = "Расписание"
    reports = "Отчеты"

    @staticmethod
    def get_list_value():
        return [name.value for name in SoftwareSection]
