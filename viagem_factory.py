from typing import Optional

from assento import Assento
from calculo_tarifa_strategy import calculo_tarifa_strategy_for
from franquia_de_bagagem import FranquiasDeBagagem
from identificadores import RegistroDeViagem, RegistroDeAeronave, CodigoVoo, SiglaAeroporto, GeradorDeRegistroDeViagem, \
    CodigoDoAssento, RegistroDePassagem
from temporal import Data, DataTempo
from viagem import Viagem


class ViagemFactory:
    gerador_de_registro: GeradorDeRegistroDeViagem
    registro: RegistroDeViagem
    data: Data

    # Aeronave
    aeronave: RegistroDeAeronave

    # Voo
    carga: float
    passageiros: int
    codigo_do_voo: CodigoVoo
    tarifa: float
    tarifa_franquia: float
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto

    # Extra
    hora_de_partida: DataTempo
    hora_de_chegada: DataTempo

    # Passagens
    assentos: dict[CodigoDoAssento, Assento]

    def __init__(self):
        self.aeronaves_possiveis = set()

    def add_tarifa_franquia(self, tarifa_franquia: float) -> "ViagemFactory":
        self.tarifa_franquia = tarifa_franquia
        return self

    def adicionar_gerador_de_registro(self, gerador_de_registro: GeradorDeRegistroDeViagem) -> "ViagemFactory":
        self.gerador_de_registro = gerador_de_registro
        return self

    def gerar_registro(self) -> "ViagemFactory":
        self.registro = self.gerador_de_registro.gerar()
        return self

    def add_data(self, data: Data) -> "ViagemFactory":
        self.data = data
        return self

    def add_voo(self, voo: "Voo") -> "ViagemFactory":
        self.carga = voo.capacidade_carga
        self.passageiros = voo.capacidade_passageiros
        self.codigo_do_voo = voo.codigo
        self.tarifa = voo.tarifa
        self.aeroporto_de_saida = voo.aeroporto_de_saida
        self.aeroporto_de_chegada = voo.aeroporto_de_chegada
        self.assentos = voo.construir_assentos()
        return self

    def add_aeronave(self, aeronave: "Aeronave") -> "ViagemFactory":
        carga = aeronave.capacidade_carga
        passageiros = aeronave.capacidade_passageiros
        if carga != self.carga or passageiros != self.passageiros:
            raise ValueError("Essa aeronave nao tem a carga e passageiros necessarios")
        self.aeronave = aeronave.registro
        return self

    def tem_assentos_liberados(self) -> bool:
        return any(map(lambda assento: assento.vazio(), self.assentos.values()))

    def assento_esta_liberado(self, assento: CodigoDoAssento) -> bool:
        if assento not in self.assentos:
            raise ValueError("Assento não encontrado")
        return self.assentos[assento].vazio()

    def tem_carga_disponivel_para_franquias(self, franquias: FranquiasDeBagagem) -> bool:
        carga_usada = 0
        for assento in self.assentos.values():
            carga_usada += assento.franquias.carga
        if carga_usada + franquias.carga() > self.carga:
            return False
        return True

    def codigo_assento_liberado(self) -> CodigoDoAssento:
        if not self.tem_assentos_liberados():
            raise ValueError("Não tem assentos liberados")
        for assento in self.assentos.values():
            if assento.vazio():
                return assento.codigo
        assert False

    def reservar_assento(self, cliente_vip: bool, registro_passagem: RegistroDePassagem, franquias: FranquiasDeBagagem,
                         assento_desejado: CodigoDoAssento) -> float:
        if not self.tem_carga_disponivel_para_franquias(franquias):
            raise ValueError("Não tem carga para franquia disponivel")
        if assento_desejado not in self.assentos:
            raise ValueError("Assento não encontrado")
        assento = self.assentos[assento_desejado]
        if assento.preenchido():
            raise ValueError("O assento está preenchido")
        assento.reservar(registro_passagem, franquias)
        return calculo_tarifa_strategy_for(cliente_vip, self.tarifa, self.tarifa_franquia).calcula(franquias)

    def liberar_assento(self, registro_passagem: RegistroDePassagem, assento: CodigoDoAssento) -> None:
        if assento not in self.assentos:
            raise ValueError("Assento não encontrado")
        assento = self.assentos[assento]
        if assento.passagem != registro_passagem:
            raise ValueError("Não foi essa passagem que reservou o assento")
        assento.liberar()

    def add_hora_de_partida_e_hora_de_chegada(self, hora_de_partida: DataTempo, hora_de_chegada: DataTempo) -> "ViagemFactory":
        self.hora_de_partida = hora_de_partida
        self.hora_de_chegada = hora_de_chegada
        return self

    def build(self):
        return Viagem(
            self.registro,
            self.codigo_do_voo,
            self.aeroporto_de_saida,
            self.aeroporto_de_chegada,
            self.hora_de_partida,
            self.hora_de_chegada,
            self.aeronave,
            self.tarifa,
            self.tarifa_franquia,
            self.assentos
        )
