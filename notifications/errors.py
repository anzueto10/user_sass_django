class InvalidNoteNotificationError(Exception):
    def __init__(self):
        super().__init__(
            "La nota de la notificación no puede estar vacía o es inválida."
        )


class InvalidNotifiedsNotificationError(Exception):
    def __init__(self):
        super().__init__("Debe haber al menos 1 notificado.")


class NotifiedsNotificatonDoNotExitsError(Exception):
    def __init__(self):
        super().__init__("Alguno de los notificados ingresados no existe.")


class InvalidAuditoriaNotificationError(Exception):
    def __init__(self):
        super().__init__("La Auditoria es inválida o está vacía, por favor corregir.")


class AuditoriaNotificationDoNotExitsError(Exception):
    def __init__(self):
        super().__init__("La Auditoria ingresada no existe.")
