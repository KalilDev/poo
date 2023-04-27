from typing import Optional, cast

from aeronave import Aeronave
from passageiro import Passageiro
from franquia_de_bagagem import FranquiasDeBagagem
from identificadores import SiglaCompanhiaAerea, RegistroDeAeronave, CodigoVoo, RegistroDeViagem, \
    GeradorDeRegistroDeViagem, SiglaAeroporto, DocumentoPassageiro, GeradorDeRegistroDePassagem, CodigoDoAssento, \
    RegistroDePassagem
from passagem import Passagem
from persist import Persist
from temporal import Data, Duracao, DataTempo, Tempo
from viagem import Viagem
from viagem_factory import ViagemFactory
from voo import Voo


class CompanhiaAerea(Persist):
    nome: str
    codigo: str
    razao_social: str
    sigla: SiglaCompanhiaAerea
    aeronaves: dict[RegistroDeAeronave, Aeronave]
    voos_planejados: dict[CodigoVoo, Voo]
    voos_em_venda: dict[Data, dict[RegistroDeViagem, ViagemFactory]]
    voos_executados: dict[RegistroDeViagem, Viagem]
    gerador_de_registro_de_viagem: GeradorDeRegistroDeViagem
    gerador_de_registro_de_passagem: GeradorDeRegistroDePassagem
    tarifa_franquia: float
    passagens: dict[RegistroDePassagem, Passagem]
    passageiros: dict[DocumentoPassageiro, Passageiro]
    local_filename: str = "companhia_aerea.txt"

    def __init__(self,
                 nome: str,
                 codigo: str,
                 razao_social: str,
                 sigla: SiglaCompanhiaAerea,
                 aeronaves: dict[RegistroDeAeronave, Aeronave],
                 voos_planejados: dict[CodigoVoo, Voo],
                 voos_em_venda: dict[Data, dict[RegistroDeViagem, ViagemFactory]],
                 voos_executados: dict[RegistroDeViagem, Viagem],
                 gerador_de_registro_de_viagem: GeradorDeRegistroDeViagem,
                 gerador_de_registro_de_passagem: GeradorDeRegistroDePassagem,
                 tarifa_franquia: float,
                 passagens: dict[RegistroDePassagem, Passagem],
                 passageiros: dict[DocumentoPassageiro, Passageiro],
                 *args):
        self.nome = nome
        self.codigo = codigo
        self.razao_social = razao_social
        self.sigla = sigla
        self.aeronaves = aeronaves
        self.voos_planejados = voos_planejados
        self.voos_em_venda = voos_em_venda
        self.voos_executados = voos_executados
        self.gerador_de_registro_de_viagem = gerador_de_registro_de_viagem
        self.gerador_de_registro_de_passagem = gerador_de_registro_de_passagem
        self.tarifa_franquia = tarifa_franquia
        self.passagens = passagens
        self.passageiros = passageiros
        super().__init__(*args)

    def registrar_que_viagem_aconteceu(self, hora_de_partida: DataTempo,
                                       hora_de_chegada: DataTempo, registro_de_viagem: RegistroDeViagem):
        fabrica: Optional[ViagemFactory] = None
        for registro_fabrica in self.voos_em_venda.values():
            if registro_de_viagem in registro_fabrica:
                fabrica = registro_fabrica[registro_de_viagem]
                del registro_fabrica[registro_de_viagem]
                break
        if fabrica is None:
            raise ValueError("Fabrica não encontrada")
        fabrica.add_hora_de_partida_e_hora_de_chegada(hora_de_partida, hora_de_chegada)
        viagem = fabrica.build()
        self.voos_executados[viagem.registro] = viagem

    def _encontrar_voos_sem_conexao(self, data: Data, aeroporto_de_saida: SiglaAeroporto,
                                    aeroporto_de_chegada: SiglaAeroporto) -> list[CodigoVoo]:
        voos = []

        def voo_desejado(voo: Voo) -> bool:
            if data.dia_da_semana not in voo.dias_da_semana:
                return False
            if aeroporto_de_saida != voo.aeroporto_de_saida:
                return False
            if aeroporto_de_chegada != voo.aeroporto_de_chegada:
                return False
            return True

        for voo in filter(voo_desejado, self.voos_planejados.values()):
            voos.append(voo.codigo)
        return voos

    def _encontrar_voos_com_conexao(self, data: Data, aeroporto_de_saida: SiglaAeroporto,
                                    aeroporto_de_chegada: SiglaAeroporto) -> list[(CodigoVoo, CodigoVoo)]:
        voos = []

        def voo_intermediario_desejado(voo: Voo) -> bool:
            if data.dia_da_semana not in voo.dias_da_semana:
                return False
            if aeroporto_de_saida != voo.aeroporto_de_saida:
                return False
            return True

        def voo_final_desejado(voo: Voo, hora_de_chegada: Tempo) -> bool:
            if data.dia_da_semana not in voo.dias_da_semana:
                return False
            if voo.aeroporto_de_chegada != aeroporto_de_chegada:
                return False
            tempo_da_conexao = hora_de_chegada + Duracao.meia_hora()
            if voo.hora_de_partida > tempo_da_conexao:
                return False
            return True

        for voo_intermediario in filter(voo_intermediario_desejado, self.voos_planejados.values()):
            for voo_final in filter(lambda voo_final:
                                    voo_final_desejado(voo_final,
                                                       voo_intermediario.hora_de_partida + voo_intermediario.duracao_estimada),
                                    self.voos_planejados.values()):
                voos.append((voo_intermediario.codigo, voo_final.codigo))
        return voos

    def _encontrar_melhor_voo(self, cliente_vip: bool, data: Data, aeroporto_de_saida: SiglaAeroporto,
                              aeroporto_de_chegada: SiglaAeroporto, franquias: FranquiasDeBagagem) -> list[CodigoVoo]:
        voos_sem_conexao = self._encontrar_voos_sem_conexao(data, aeroporto_de_saida, aeroporto_de_chegada)
        infinity = 1 / 0
        melhor_tarifa = infinity
        if len(voos_sem_conexao) != 0:
            melhor_voo = None
            for codigo_voo in voos_sem_conexao:
                voo = self.voos_planejados[codigo_voo]
                tarifa = voo.calcula_tarifa(cliente_vip, franquias, self.tarifa_franquia)
                if tarifa >= melhor_tarifa:
                    continue
                melhor_voo = voo
                melhor_tarifa = tarifa
            return [melhor_voo.codigo]
        infinity = 1 / 0
        melhor_tarifa = infinity
        pares_de_voos = self._encontrar_voos_com_conexao(data, aeroporto_de_saida, aeroporto_de_chegada)
        if len(pares_de_voos) == 0:
            return []
        (melhor_voo_intermediario, melhor_voo_final) = (None, None)
        for (codigo_voo_intermediario, codigo_voo_final) in pares_de_voos:
            voo_intermediario = self.voos_planejados[codigo_voo_intermediario]
            voo_final = self.voos_planejados[codigo_voo_final]
            tarifa_intermediario = voo_intermediario.calcula_tarifa(cliente_vip, franquias, self.tarifa_franquia)
            tarifa_final = voo_final.calcula_tarifa(cliente_vip, franquias, self.tarifa_franquia)
            tarifa = tarifa_intermediario + tarifa_final
            if tarifa >= melhor_tarifa:
                continue
            melhor_voo_intermediario = voo_intermediario
            melhor_voo_final = voo_final
            melhor_tarifa = tarifa
        return [melhor_voo_intermediario.codigo, melhor_voo_final.codigo]

    def adicionar_viagens_em_venda(self):
        datas_atuais = set(self.voos_em_venda.keys())
        hoje = Data.now()
        datas_alvo = set(map(lambda i: hoje + Duracao.um_dia() * i, range(30)))
        datas_nao_preenchidas = datas_alvo - datas_atuais
        for data in datas_nao_preenchidas:
            voos_nesse_dia_da_semana = filter(lambda voo: data.dia_da_semana in voo.dias_da_semana,
                                              self.voos_planejados.values())
            viagens_nesse_dia_da_semana = self.voos_em_venda[data] = {}
            for voo_que_ira_acontecer in voos_nesse_dia_da_semana:
                viagem_factory = ViagemFactory() \
                    .add_tarifa_franquia(self.tarifa_franquia) \
                    .adicionar_gerador_de_registro(self.gerador_de_registro_de_viagem) \
                    .gerar_registro() \
                    .add_data(data) \
                    .add_voo(voo_que_ira_acontecer)
                registro_da_viagem = viagem_factory.registro
                viagens_nesse_dia_da_semana[registro_da_viagem] = viagem_factory

    def cancelar_passagem(self, passagem: RegistroDePassagem):
        if passagem not in self.passagens:
            raise ValueError("Passagem não está na companhia")
        passagem = self.passagens[passagem]
        data = passagem.data
        for viagem, assento in passagem.assentos.items():
            voos_em_venda_na_data = self.voos_em_venda[data]
            if viagem not in voos_em_venda_na_data:
                raise ValueError("Não é possivel cancelar uma viagem que já ocorreu")
            viagem = voos_em_venda_na_data[viagem]
            viagem.liberar_assento(passagem.registro, assento)
        id_cliente = passagem.documento_cliente
        cliente = self.passageiros[id_cliente]
        cliente.passagens.remove(passagem.registro)
        del self.passagens[passagem.registro]
        return

    def comprar_passagem(self, id_cliente: DocumentoPassageiro, data: Data, aeroporto_de_saida: SiglaAeroporto,
                         aeroporto_de_chegada: SiglaAeroporto, franquias: FranquiasDeBagagem,
                         assento: Optional[CodigoDoAssento]) -> Optional[RegistroDePassagem]:
        if id_cliente not in self.passageiros:
            raise ValueError("Cliente nao cadastrado")
        cliente = self.passageiros[id_cliente]
        voos = self._encontrar_melhor_voo(cliente.vip, data, aeroporto_de_saida, aeroporto_de_chegada, franquias)
        if len(voos) == 0:
            return None

        def find_voo(codigo_voo: CodigoVoo) -> Optional[ViagemFactory]:
            viagem_factories = self.voos_em_venda[data]
            for viagem_factory in viagem_factories.values():
                if viagem_factory.codigo_do_voo == codigo_voo:
                    return viagem_factory
            return None

        viagem_factories = map(find_voo, voos)
        if len(list(filter(lambda viagem_factory: viagem_factories == None, viagem_factories))) != 0:
            return None
        for viagem_factory in viagem_factories:
            if assento is None:
                if not viagem_factory.tem_assentos_liberados():
                    return None
            elif not viagem_factory.assento_esta_liberado(assento):
                return None
            if not viagem_factory.tem_carga_disponivel_para_franquias(franquias):
                return None
        registro_passagem = self.gerador_de_registro_de_passagem.gerar()
        viagens_assentos = {}
        valor_total = 0
        for viagem_factory in viagem_factories:
            assento_desejado = cast(CodigoDoAssento, assento or viagem_factory.codigo_assento_liberado())
            valor = viagem_factory.reservar_assento(cliente.vip, registro_passagem, franquias, assento_desejado)
            valor_total += valor
            viagens_assentos[viagem_factory.registro] = assento_desejado
        passagem = Passagem(
            registro_passagem,
            self.voos_planejados[voos[0]].aeroporto_de_saida,
            self.voos_planejados[voos[-1]].aeroporto_de_chegada,
            self.sigla,
            id_cliente,
            data,
            valor_total,
            viagens_assentos,
            DataTempo.now()
        )
        cliente.passagens.append(passagem.registro)
        self.passagens[registro_passagem] = passagem

    def acessar_historico_de_viagens(self, passageiro: DocumentoPassageiro) -> list[Viagem]:
        if passageiro not in self.passageiros:
            raise ValueError("Passageiro nao cadastrado")
        passageiro = self.passageiros[passageiro]
        regisgros_de_passagens = passageiro.passagens
        passagens = map(lambda passagem: cast(Passagem, self.passagens[passagem]), regisgros_de_passagens)
        viagens = []
        for passagem in passagens:
            registros_de_viagens = passagem.assentos.keys()
            viagens_na_passagem = map(lambda registro_de_viagem: self.voos_executados[registro_de_viagem], registros_de_viagens)
            for viagem in viagens_na_passagem:
                viagens.append(viagem)
        viagens.sort()
        return viagens


    @staticmethod
    def get_records_by_field(field, value):
        return Persist.get_records_by_field(field, value, CompanhiaAerea)

    @staticmethod
    def get_records():
        return Persist.get_records(CompanhiaAerea)

    @staticmethod
    def get_filename():
        return CompanhiaAerea.local_filename
