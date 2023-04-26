from identificadores import SiglaCompanhiaAerea, RegistroDeAeronave


class Aeronave:
    companhia_aerea: SiglaCompanhiaAerea
    fabricante: str
    modelo: str
    capacidade_passageiros: int
    capacidade_carga: float
    registro: RegistroDeAeronave

    def __init__(self,
                 companhia_aerea: SiglaCompanhiaAerea,
                 fabricante: str,
                 modelo: str,
                 capacidade_passageiros: int,
                 capacidade_carga: float,
                 registro: RegistroDeAeronave,
                 ):
        self.companhia_aerea = companhia_aerea
        self.fabricante = fabricante
        self.modelo = modelo
        self.capacidade_passageiros = capacidade_passageiros
        self.capacidade_carga = capacidade_carga
        self.registro = registro
