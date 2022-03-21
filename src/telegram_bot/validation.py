def validate_first_name_and_last_name(value: str) -> bool:
    """Имя и фамилия представлены строкой разделенной пробелом"""
    try:
        first_name, last_name = value.split(" ")
        if first_name.isalpha() and last_name.isalpha():
            return True
    except:
        return False


def validate_position(value: str) -> bool:
    """Профессия должна состоять только из букв, может содержать пробелы"""
    try:
        if " " in value:
            values = value.split(" ")
            for value in values:
                if not value.isalpha():
                    return False
            return True
        if value.isalpha():
            return True
    except:
        return False
