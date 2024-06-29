class InvalidAuditoriaTitleError(Exception):
    def __init__(self):
        super.__init__("El título de la auditoria no puede ser vacío o es inválido.")


class InvalidAuditoriaDescriptionError(Exception):
    def __init__(self):
        super.__init__(
            "La descripsión de la auditoria no puede ser vacía o es inválida."
        )


class InvalidAuditoriaCompanyError(Exception):
    def __init__(self):
        super.__init__(
            "El nombre de la compañía de la auditoria no puede ser vacío o es inválido."
        )


class InvalidAuditoriaAuditoresError(Exception):
    def __init__(self):
        super.__init__("Los auditores asignados son inválidos o no existen.")


class InvalidAuditoriaSupervisoresError(Exception):
    def __init__(self):
        super.__init__("Los supervisores asignados no existen o son inválidos.")
