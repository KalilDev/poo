from pydantic import BaseModel

from aeronave import RegistroDeAeronave
from aeroporto import SiglaAeroporto
from companhia_aerea import SiglaCompanhiaAerea
from persist import Persist
from temporal import Tempo, DiaDaSemana, Duracao, DataTempo


class PlanejamentoDeVoo(Persist):
    companhia_aerea: SiglaCompanhiaAerea
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto
    hora_de_partida: Tempo
    duracao_estimada: Duracao
    dias_da_semana: set[DiaDaSemana]
    aeronave_padrao: RegistroDeAeronave
