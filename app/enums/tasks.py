from enum import Enum

class ImportanceStatusTask(str, Enum):
    first_level: str = "Не срочная задача"
    second_level: str = "Срочная задача"
    third_level: str = "Очень срочная задача"