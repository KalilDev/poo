from typing import Optional

from franquia_de_bagagem import FranquiasDeBagagem
from identificadores import CodigoDoAssento, RegistroDePassagem


class Assento:
    codigo: CodigoDoAssento
    passagem: Optional[RegistroDePassagem]
    franquias: Optional[FranquiasDeBagagem]

    def __init__(self, codigo: CodigoDoAssento):
        self.codigo = codigo
        self.passagem = None
        self.franquias = None

    def classe(self):
        return self.codigo.classe

    def preenchido(self) -> bool:
        return self.passagem is not None or self.franquias is not None

    def vazio(self) -> bool:
        return not self.preenchido()

    def liberar(self) -> (RegistroDePassagem, FranquiasDeBagagem):
        if not self.preenchido():
            raise ValueError("O assento não está preenchido")
        passagem = self.passagem
        self.passagem = None
        franquias = self.franquias
        self.franquias = None
        return passagem, franquias

    def reservar(self, passagem: RegistroDePassagem, franquias: FranquiasDeBagagem) -> None:
        if self.preenchido():
            raise ValueError("O assento está preenchido")
        self.passagem = passagem
        self.franquias = franquias
