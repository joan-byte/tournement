from fastapi import HTTPException, status

class DominoException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class CampeonatoException(DominoException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class ParejaException(DominoException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class ResultadoException(DominoException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class MesaException(DominoException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class PartidaException(DominoException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class NotFoundError(DominoException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ValidationError(DominoException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class DatabaseError(DominoException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail) 