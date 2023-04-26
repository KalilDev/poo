from estado import Estado
from identificadores import SiglaAeroporto


class Aeroporto:
    sigla: SiglaAeroporto
    cidade: str
    estado: Estado

    def __init__(self,
                 sigla: SiglaAeroporto,
                 cidade: str,
                 estado: Estado,
                 ):
        self.sigla = sigla
        self.cidade = cidade
        self.estado = estado
