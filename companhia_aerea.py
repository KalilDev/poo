from aeronave import Aeronave
from identificadores import SiglaCompanhiaAerea, RegistroDeAeronave
from persist import Persist
from planejamento_de_voo import PlanejamentoDeVoo
from voo import RegistroDeVoo, Voo


class CompanhiaAerea(Persist):
    nome: str
    codigo: str
    razao_social: str
    sigla: SiglaCompanhiaAerea
    aeronaves: dict[RegistroDeAeronave, Aeronave]
    voos_planejados: list[PlanejamentoDeVoo]
    voos_executados: dict[RegistroDeVoo, Voo]
    local_filename: str = "companhia_aerea.txt"

    def __init__(self,
                 nome: str,
                 codigo: str,
                 razao_social: str,
                 sigla: SiglaCompanhiaAerea,
                 aeronaves: dict[RegistroDeAeronave, Aeronave],
                 voos_planejados: list[PlanejamentoDeVoo],
                 voos_executados: dict[RegistroDeVoo, Voo],
                 *args):
        self.nome = nome
        self.codigo = codigo
        self.razao_social = razao_social
        self.sigla = sigla
        self.aeronaves = aeronaves
        self.voos_planejados = voos_planejados
        self.voos_executados = voos_executados
        super().__init__(*args)

    @staticmethod
    def get_records_by_field(field, value):
        return Persist.get_records_by_field(field, value, CompanhiaAerea)

    @staticmethod
    def get_records():
        return Persist.get_records(CompanhiaAerea)

    @staticmethod
    def get_filename():
        return CompanhiaAerea.local_filename
