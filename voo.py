from aeroporto import SiglaAeroporto
from assento import Assento
from calculo_tarifa_strategy import calculo_tarifa_strategy_for
from companhia_aerea import SiglaCompanhiaAerea
from franquia_de_bagagem import FranquiasDeBagagem
from identificadores import RegistroDeAeronave, CodigoVoo, GeradorDeCodigoDoAssento, CodigoDoAssento
from temporal import Tempo, DiaDaSemana, Duracao


class Voo:
    codigo: CodigoVoo
    companhia_aerea: SiglaCompanhiaAerea
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto
    hora_de_partida: Tempo
    duracao_estimada: Duracao
    dias_da_semana: set[DiaDaSemana]
    aeronave_padrao: RegistroDeAeronave
    capacidade_passageiros: int
    capacidade_carga: float
    tarifa: float

    def __init__(self,
                 codigo: CodigoVoo,
                 companhia_aerea: SiglaCompanhiaAerea,
                 aeroporto_de_saida: SiglaAeroporto,
                 aeroporto_de_chegada: SiglaAeroporto,
                 hora_de_partida: Tempo,
                 duracao_estimada: Duracao,
                 dias_da_semana: set[DiaDaSemana],
                 aeronave_padrao: RegistroDeAeronave,
                 capacidade_passageiros: int,
                 capacidade_carga: float,
                 tarifa: float,
                 ):
        self.codigo = codigo
        self.companhia_aerea = companhia_aerea
        self.aeroporto_de_saida = aeroporto_de_saida
        self.aeroporto_de_chegada = aeroporto_de_chegada
        self.hora_de_partida = hora_de_partida
        self.duracao_estimada = duracao_estimada
        self.dias_da_semana = dias_da_semana
        self.aeronave_padrao = aeronave_padrao
        self.capacidade_passageiros = capacidade_passageiros
        self.capacidade_carga = capacidade_carga
        self.tarifa = tarifa

    def calcula_tarifa(self, cliente_vip: bool, franquias: FranquiasDeBagagem, tarifa_franquia: float) -> float:
        return calculo_tarifa_strategy_for(cliente_vip, self.tarifa, tarifa_franquia).calcula(franquias)

    def construir_assentos(self) -> dict[CodigoDoAssento, Assento]:
        gerador = GeradorDeCodigoDoAssento(self.capacidade_passageiros, 0.0)
        assentos = gerador.gerar_todos()
        dict_assentos = {}
        for codigo_assento in assentos:
            dict_assentos[codigo_assento] = Assento(codigo_assento)
        return dict_assentos
