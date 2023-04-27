from enum import Enum

from identificadores import SiglaAeroporto, SiglaCompanhiaAerea, RegistroDeViagem, RegistroDePassagem, CodigoDoAssento, \
    DocumentoPassageiro
from temporal import Data, DataTempo

class StatusDaPassagem:
    class Tipo(str, Enum):
        CANCELADA = "cancelada"
        CHECK_IN_NAO_ABERTO = "check_in_nao_aberto"
        AGUARDANDO_CHECK_IN = "aguardando_check_in"
        NAO_APARECEU = "nao_apareceu"
        CHECKED_IN = "checked_in"
        EMBARCADO = "embarcado"
        CONCLUIDA_COM_SUCESSO = "concluida_com_sucesso"

    class Evento(str, Enum):
        CANCELAR = "cancelar"
        ABRIR_CHECK_IN = "abrir_check_in"
        FAZER_CHECK_IN = "fazer_check_in"
        EMBARCAR = "embarcar"
        CONCLUIR = "concluir"

    tipo: Tipo
    def __init__(self, tipo: Tipo):
        self.tipo = tipo
    def cancelar(self) -> "StatusDaPassagem":
        return self
    def abrir_check_in(self) -> "StatusDaPassagem":
        return self
    def fazer_check_in(self) -> "StatusDaPassagem":
        return self
    def embarcar(self) -> "StatusDaPassagem":
        return self
    def concluir(self) -> "StatusDaPassagem":
        return self

    def dispatch_event(self, evento: Evento) -> "StatusDaPassagem":
        match evento:
            case StatusDaPassagem.Evento.CANCELAR: return self.cancelar()
            case StatusDaPassagem.Evento.ABRIR_CHECK_IN: return self.abrir_check_in()
            case StatusDaPassagem.Evento.FAZER_CHECK_IN: return self.fazer_check_in()
            case StatusDaPassagem.Evento.EMBARCAR: return self.embarcar()
            case StatusDaPassagem.Evento.CONCLUIR: return self.concluir()
        assert False

class PassagemCancelada(StatusDaPassagem):
    def __init__(self):
        super().__init__(StatusDaPassagem.Tipo.CANCELADA)
    # Don't transition to any state

class PassagemCheckInNaoAberto(StatusDaPassagem):
    def __init__(self):
        super().__init__(StatusDaPassagem.Tipo.CHECK_IN_NAO_ABERTO)
    # Transition to cancelled or to checkin aberto
    def cancelar(self) -> "StatusDaPassagem":
        return PassagemCancelada()
    def abrir_check_in(self) -> "StatusDaPassagem":
        return PassagemAguardandoCheckIn()
class PassagemAguardandoCheckIn(StatusDaPassagem):
    def __init__(self):
        super().__init__(StatusDaPassagem.Tipo.AGUARDANDO_CHECK_IN)
    # Transition to cancelled, checked in or did not show up
    def cancelar(self) -> "StatusDaPassagem":
        return PassagemCancelada()
    def fazer_check_in(self) -> "StatusDaPassagem":
        return PassagemCheckedIn()
    def concluir(self) -> "StatusDaPassagem":
        return PassagemNaoApareceu()

class PassagemNaoApareceu(StatusDaPassagem):
    def __init__(self):
        super().__init__(StatusDaPassagem.Tipo.NAO_APARECEU)
    # Dont transition

class PassagemCheckedIn(StatusDaPassagem):
    def __init__(self):
        super().__init__(StatusDaPassagem.Tipo.CHECKED_IN)
    # Transition to no show, cancelled or embarcated
    def embarcar(self) -> "StatusDaPassagem":
        return PassagemEmbarcado()
    def cancelar(self) -> "StatusDaPassagem":
        return PassagemCancelada()
    def concluir(self) -> "StatusDaPassagem":
        return PassagemNaoApareceu()

class PassagemEmbarcado(StatusDaPassagem):
    def __init__(self):
        super().__init__(StatusDaPassagem.Tipo.EMBARCADO)
    # Transition to concluded
    def concluir(self) -> "StatusDaPassagem":
        return PassagemConcluidaComSucesso()

class PassagemConcluidaComSucesso(StatusDaPassagem):
    def __init__(self):
        super().__init__(StatusDaPassagem.Tipo.CONCLUIDA_COM_SUCESSO)
    # Dont transition

class Passagem:
    registro: RegistroDePassagem
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto
    companhia_aerea: SiglaCompanhiaAerea
    documento_cliente: DocumentoPassageiro
    data: Data
    valor: float
    valor_pago: float
    assentos: dict[RegistroDeViagem, CodigoDoAssento]
    data_tempo_de_compra: DataTempo
    status: StatusDaPassagem

    def __init__(self,
                 registro: RegistroDePassagem,
                 aeroporto_de_saida: SiglaAeroporto,
                 aeroporto_de_chegada: SiglaAeroporto,
                 companhia_aerea: SiglaCompanhiaAerea,
                 documento_cliente: DocumentoPassageiro,
                 data: Data,
                 valor: float,
                 valor_pago: float,
                 assentos: dict[RegistroDeViagem, CodigoDoAssento],
                 data_tempo_de_compra: DataTempo,
                 status: StatusDaPassagem
                 ):
        self.registro = registro
        self.aeroporto_de_saida = aeroporto_de_saida
        self.aeroporto_de_chegada = aeroporto_de_chegada
        self.companhia_aerea = companhia_aerea
        self.documento_cliente = documento_cliente
        self.data = data
        self.valor = valor
        self.valor_pago = valor_pago
        self.assentos = assentos
        self.data_tempo_de_compra = data_tempo_de_compra
        self.status = status

    def tipo_de_status(self) -> StatusDaPassagem.Tipo:
        return self.status.tipo

    def valor_devendo(self) -> float:
        return self.valor - self.valor_pago

    def pagar(self, valor: float) -> float:
        if self.valor_devendo() < valor:
            raise ValueError("Você tá pagando muito, a companhia não pode ficar te devendo")
        self.valor_pago += valor
        return self.valor_devendo()

    def acionar_evento(self, evento: StatusDaPassagem.Evento) -> bool:
        old_status = self.status
        new_status = self.status.dispatch_event(evento)
        self.status = new_status
        return old_status == new_status
    #def alterar_status(self, status: StatusDaPassagem) -> bool:
    #    match self.status:
    #        case StatusDaPassagem.CANCELADA:
    #            return False
    #        case StatusDaPassagem.CHECK_IN_NAO_ABERTO:
    #            if status != StatusDaPassagem.AGUARDANDO_CHECK_IN or status != StatusDaPassagem.CANCELADA:
    #                return False
    #        case StatusDaPassagem.AGUARDANDO_CHECK_IN:
    #            if status != StatusDaPassagem.CANCELADA or status != StatusDaPassagem.NAO_APARECEU:
    #                return False
    #        case StatusDaPassagem.NAO_APARECEU:
    #            return False
    #        case StatusDaPassagem.CHECKED_IN:
    #            if status != StatusDaPassagem.CONCLUIDA_COM_SUCESSO or status != StatusDaPassagem.NAO_APARECEU:
    #                return False
    #        case StatusDaPassagem.EMBARCADO:
    #            if status != StatusDaPassagem.CONCLUIDA_COM_SUCESSO:
    #                return False
    #        case StatusDaPassagem.CONCLUIDA_COM_SUCESSO:
    #            return False
    #    status = status
    #    return True