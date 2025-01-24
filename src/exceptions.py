class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"

class AllRoomsAreBookedException(NabronirovalException):
    detail = "Нет свободных номеров"

class WrongDateException(NabronirovalException):
    detail = "Дата заезда должна быть раньше, чем дата выезда"
