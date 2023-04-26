from enum import Enum

from pydantic import BaseModel, validator

from companhia_aerea import SiglaCompanhiaAerea


class PrefixoRegistroDeAeronave(str, Enum):
    PT = "PT"
    PR = "PR"
    PP = "PP"
    PS = "PS"


class RegistroDeAeronave(BaseModel):
    prefixo: PrefixoRegistroDeAeronave
    sufixo: str

    def __init__(self, prefixo: PrefixoRegistroDeAeronave, sufixo: str):
        super().__init__(prefixo=prefixo, sufixo=sufixo)

    def __str__(self):
        return f"{self.prefixo.value}-{self.sufixo}"

    @validator("sufixo")
    def valida_sufixo(cls, v: str):
        if len(v) != 3:
            raise ValueError("O sufixo deve ter 3 letras")
        if not v.isupper():
            raise ValueError("O sufixo deve ser uppercase")
        if not v.isalpha():
            raise ValueError("O sufixo deve ser composto somente por letras")
        return v


class Aeronave:
    companhia_aerea: SiglaCompanhiaAerea
    fabricante: str
    modelo: str
    capacidade_passageiros: int
    capacidade_carga: float
    registro: RegistroDeAeronave
