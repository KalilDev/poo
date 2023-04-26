from pydantic import validator, BaseModel

from aeronave import RegistroDeAeronave
from aeroporto import SiglaAeroporto
from companhia_aerea import SiglaCompanhiaAerea
from temporal import DataTempo


class RegistroDeVoo(BaseModel):
    prefixo: str
    numero: int

    def __init__(self, prefixo: str, numero: int):
        super().__init__(prefixo=prefixo, numero=numero)

    def __str__(self):
        return f"{self.prefixo}{self.numero:0>4}"

    @validator("prefixo")
    def valida_prefixo(cls, v: str):
        if len(v) != 2:
            raise ValueError("O prefixo deve ter dois caracteres")
        if not v.isupper():
            raise ValueError("O prefixo deve ser uppercase")
        if not v.isalpha():
            raise ValueError("O prefixo deve ser feito de letras")
        return v

    @validator("numero")
    def valida_numero(cls, v: int):
        if v < 0:
            raise ValueError("O numero é negativo")
        if v > 9999:
            raise ValueError("O numero é muito grande")
        return v


class Voo:
    registro: RegistroDeVoo
    companhia_aerea: SiglaCompanhiaAerea
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto
    hora_de_partida: DataTempo
    hora_de_chegada: DataTempo
    aeronave: RegistroDeAeronave
