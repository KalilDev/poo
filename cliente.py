from identificadores import DocumentoCliente
from persist import Persist


class Cliente(Persist):
    nome: str
    sobrenome: str
    documento: DocumentoCliente
    local_filename: str = "cliente.txt"

    def __init__(self, nome: str, sobrenome: str, documento: DocumentoCliente, *args):
        self.nome = nome
        self.sobrenome = sobrenome
        self.documento = documento
        super().__init__(*args)

    @staticmethod
    def get_records_by_field(field, value):
        return Persist.get_records_by_field(field, value, Cliente)

    @staticmethod
    def get_records():
        return Persist.get_records(Cliente)

    @staticmethod
    def get_filename():
        return Cliente.local_filename