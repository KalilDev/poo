from enum import Enum

from pydantic import BaseModel, validator


class SiglaCompanhiaAerea(BaseModel):
    sigla: str

    def __init__(self, sigla: str):
        super().__init__(sigla=sigla)

    def __str__(self):
        return self.sigla

    @validator("sigla")
    def valida_sigla(cls, v: str):
        if len(v) != 2:
            raise ValueError("Sigla invalida")
        return v


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


class RegistroDeVoo(BaseModel):
    prefixo: str
    numero: int

    def __init__(self, prefixo: str, numero: int):
        super().__init__(prefixo=prefixo, numero=numero)

    def __str__(self):
        return f"{self.prefixo}{self.numero:0>4}"

    @validator("prefixo")
    def valida_prefixo(self, v: str):
        if len(v) != 2:
            raise ValueError("O prefixo deve ter dois caracteres")
        if not v.isupper():
            raise ValueError("O prefixo deve ser uppercase")
        if not v.isalpha():
            raise ValueError("O prefixo deve ser feito de letras")
        return v

    @validator("numero")
    def valida_numero(self, v: int):
        if v < 0:
            raise ValueError("O numero é negativo")
        if v > 9999:
            raise ValueError("O numero é muito grande")
        return v


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
