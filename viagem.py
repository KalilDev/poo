from assento import Assento
from identificadores import RegistroDeViagem, RegistroDeAeronave, SiglaCompanhiaAerea, SiglaAeroporto, CodigoVoo, \
    CodigoDoAssento
from temporal import DataTempo


class Viagem:
    registro: RegistroDeViagem
    codigo_do_voo: CodigoVoo
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto
    hora_de_partida: DataTempo
    hora_de_chegada: DataTempo
    aeronave: RegistroDeAeronave
    tarifa: float
    tarifa_franquia: float
    assentos: dict[CodigoDoAssento, Assento]

    def __init__(self,
                 registro: RegistroDeViagem,
                 codigo_do_voo: CodigoVoo,
                 aeroporto_de_saida: SiglaAeroporto,
                 aeroporto_de_chegada: SiglaAeroporto,
                 hora_de_partida: DataTempo,
                 hora_de_chegada: DataTempo,
                 aeronave: RegistroDeAeronave,
                 tarifa: float,
                 tarifa_franquia: float,
                 assentos: dict[CodigoDoAssento, Assento],
                 ):
        self.registro = registro
        self.codigo_do_voo = codigo_do_voo
        self.aeroporto_de_saida = aeroporto_de_saida
        self.aeroporto_de_chegada = aeroporto_de_chegada
        self.hora_de_partida = hora_de_partida
        self.hora_de_chegada = hora_de_chegada
        self.aeronave = aeronave
        self.tarifa = tarifa
        self.tarifa_franquia = tarifa_franquia
        self.assentos = assentos

    def __gt__(self, other: "Viagem"):
        return self.hora_de_partida > other.hora_de_partida

    def __lt__(self, other: "Viagem"):
        return self.hora_de_partida < other.hora_de_partida