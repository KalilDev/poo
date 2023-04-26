from aeroporto import SiglaAeroporto
from companhia_aerea import SiglaCompanhiaAerea
from identificadores import RegistroDeAeronave
from temporal import Tempo, DiaDaSemana, Duracao


class PlanejamentoDeVoo:
    companhia_aerea: SiglaCompanhiaAerea
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto
    hora_de_partida: Tempo
    duracao_estimada: Duracao
    dias_da_semana: set[DiaDaSemana]
    aeronave_padrao: RegistroDeAeronave

    def __init__(self,
                 companhia_aerea: SiglaCompanhiaAerea,
                 aeroporto_de_saida: SiglaAeroporto,
                 aeroporto_de_chegada: SiglaAeroporto,
                 hora_de_partida: Tempo,
                 duracao_estimada: Duracao,
                 dias_da_semana: set[DiaDaSemana],
                 aeronave_padrao: RegistroDeAeronave,
                 ):
        self.companhia_aerea = companhia_aerea
        self.aeroporto_de_saida = aeroporto_de_saida
        self.aeroporto_de_chegada = aeroporto_de_chegada
        self.hora_de_partida = hora_de_partida
        self.duracao_estimada = duracao_estimada
        self.dias_da_semana = dias_da_semana
        self.aeronave_padrao = aeronave_padrao
