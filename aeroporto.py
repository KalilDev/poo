from pydantic import BaseModel, validator

from estado import Estado
from persist import Persist


class SiglaAeroporto(BaseModel):
    sigla: str
    def __init__(self, sigla: str):
        super().__init__(sigla=sigla)
    def __str__(self):
        return self.sigla
    @validator("sigla")
    def valida_sigla(self, v: str):
        if len(v) != 3:
            raise ValueError("A sigla deve ter 3 caracteres")
        if not v.isupper():
            raise ValueError("A sigla deve ser uppercase")
        if not v.isalpha():
            raise ValueError("A sigla deve ser feita de caracteres")
        return v

class Aeroporto(Persist):
    sigla: SiglaAeroporto
    cidade: str
    estado: Estado