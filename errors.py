class Missing(Exception):
    """Exception raised for missing items."""  # Докстрока для класса исключения Missing

    def __init__(self, name: str, message: str = None):
        self.name = name  # Имя пропавшего элемента
        self.message = message or f"{name} is missing."  # Сообщение об ошибке с поддержкой сообщения по умолчанию
        super().__init__(self.message)  # Инициализация базового класса Exception

    def __str__(self):
        return self.message  # Возвращает строковое представление исключения


class Duplicate(Exception):
    """Exception raised for duplicate items."""  # Докстрока для класса исключения Duplicate

    def __init__(self, name: str, message: str = None):
        self.name = name  # Имя дублирующегося элемента
        self.message = message or f"{name} already exists."  # Сообщение об ошибке с поддержкой сообщения по умолчанию
        super().__init__(self.message)  # Инициализация базового класса Exception

    def __str__(self):
        return self.message  # Возвращает строковое представление исключения
