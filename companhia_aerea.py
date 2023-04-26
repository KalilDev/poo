from pydantic import BaseModel, validator

from aeronave import Aeronave, RegistroDeAeronave
from persist import Persist
from planejamento_de_voo import PlanejamentoDeVoo
from voo import RegistroDeVoo, Voo


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


class CompanhiaAerea(Persist):
    nome: str
    codigo: str
    razao_social: str
    sigla: SiglaCompanhiaAerea
    aeronaves: dict[RegistroDeAeronave, Aeronave]
    voos_planejados: list[PlanejamentoDeVoo]
    voos_executados: dict[RegistroDeVoo, Voo]
