from typing import Optional

from pydantic import BaseModel, validator

from identificadores import DocumentoPassageiro, Email, CPF, RegistroDePassagem
from nacionalidades import Nacionalidade
from temporal import Data


class Passageiro(BaseModel):
    nome: str
    sobrenome: str
    documento: DocumentoPassageiro
    nacionalidade: str
    cpf: Optional[CPF]
    data_de_nascimento: Data
    email: Email
    passagens: list[RegistroDePassagem]
    vip: bool

    def __init__(self,
                 nome: str,
                 sobrenome: str,
                 documento: DocumentoPassageiro,
                 nacionalidade: str,
                 cpf: Optional[CPF],
                 data_de_nascimento: Data,
                 email: Email,
                 passagens: list[RegistroDePassagem],
                 vip: bool):
        super().__init__(
            nome = nome,
            sobrenome = sobrenome,
            documento = documento,
            nacionalidade = nacionalidade,
            cpf = cpf,
            data_de_nascimento = data_de_nascimento,
            email = email,
            passagens = passagens,
            vip = vip,
        )

    @validator('cpf')
    def valida_cpf_se_brasileiro(self, cpf: Optional[CPF], values):
        if values['nacionalidade'] == Nacionalidade.BRASIL and cpf is None:
            raise ValueError('O CPF deve ser definido para brasileiros')
        if values['nacionalidade'] != Nacionalidade.BRASIL and cpf is not None:
            raise ValueError('O CPF deve ser definido somente para brasileiros')
        return cpf