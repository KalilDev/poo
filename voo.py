from identificadores import RegistroDeVoo, RegistroDeAeronave, SiglaCompanhiaAerea, SiglaAeroporto
from temporal import DataTempo


class Voo:
    registro: RegistroDeVoo
    companhia_aerea: SiglaCompanhiaAerea
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto
    hora_de_partida: DataTempo
    hora_de_chegada: DataTempo
    aeronave: RegistroDeAeronave

    def __init__(self,
                 registro: RegistroDeVoo,
                 companhia_aerea: SiglaCompanhiaAerea,
                 aeroporto_de_saida: SiglaAeroporto,
                 aeroporto_de_chegada: SiglaAeroporto,
                 hora_de_partida: DataTempo,
                 hora_de_chegada: DataTempo,
                 aeronave: RegistroDeAeronave,
                 ):
        self.registro = registro
        self.companhia_aerea = companhia_aerea
        self.aeroporto_de_saida = aeroporto_de_saida
        self.aeroporto_de_chegada = aeroporto_de_chegada
        self.hora_de_partida = hora_de_partida
        self.hora_de_chegada = hora_de_chegada
        self.aeronave = aeronave
