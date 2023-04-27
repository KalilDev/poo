from identificadores import SiglaAeroporto, SiglaCompanhiaAerea, RegistroDeViagem, RegistroDePassagem, CodigoDoAssento, \
    DocumentoCliente
from temporal import Data, DataTempo


class Passagem:
    registro: RegistroDePassagem
    aeroporto_de_saida: SiglaAeroporto
    aeroporto_de_chegada: SiglaAeroporto
    companhia_aerea: SiglaCompanhiaAerea
    documento_cliente: DocumentoCliente
    data: Data
    valor: float
    assentos: dict[RegistroDeViagem, CodigoDoAssento]
    data_tempo_de_compra: DataTempo

    def __init__(self,
                 registro: RegistroDePassagem,
                 aeroporto_de_saida: SiglaAeroporto,
                 aeroporto_de_chegada: SiglaAeroporto,
                 companhia_aerea: SiglaCompanhiaAerea,
                 documento_cliente: DocumentoCliente,
                 data: Data,
                 valor: float,
                 assentos: dict[RegistroDeViagem, CodigoDoAssento],
                 data_tempo_de_compra: DataTempo
                 ):
        self.registro = registro
        self.aeroporto_de_saida = aeroporto_de_saida
        self.aeroporto_de_chegada = aeroporto_de_chegada
        self.companhia_aerea = companhia_aerea
        self.documento_cliente = documento_cliente
        self.data = data
        self.valor = valor
        self.assentos = assentos
        self.data_tempo_de_compra = data_tempo_de_compra
