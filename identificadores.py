from enum import Enum
from math import ceil
from typing import Optional, Tuple

from pydantic import BaseModel, validator

from estado import Estado


class SiglaCompanhiaAerea(BaseModel):
    sigla: str

    def __init__(self, sigla: str):
        super().__init__(sigla=sigla)

    def __str__(self):
        return self.sigla

    @validator("sigla")
    def valida_sigla(cls, v: str):
        if len(v) != 2:
            raise ValueError("Sigla invalida")
        return v


class CodigoVoo(BaseModel):
    sigla_da_comapanhia: SiglaCompanhiaAerea
    numero: int

    def __init__(self,
                 sigla_da_comapanhia: SiglaCompanhiaAerea,
                 numero: int):
        super().__init__(sigla_da_comapanhia=sigla_da_comapanhia, numero=numero)

    def __str__(self):
        return f"{self.sigla_da_comapanhia}{self.numero:0>4}"

    @validator("numero")
    def valida_numero(self, v: int):
        if v < 0:
            raise ValueError("O numero é negativo")
        if v > 9999:
            raise ValueError("O numero é muito grande")
        return v


class PrefixoRegistroDeAeronave(str, Enum):
    PT = "PT"
    PR = "PR"
    PP = "PP"
    PS = "PS"


class RegistroDeAeronave(BaseModel):
    prefixo: PrefixoRegistroDeAeronave
    sufixo: str

    def __init__(self, prefixo: PrefixoRegistroDeAeronave, sufixo: str):
        super().__init__(prefixo=prefixo, sufixo=sufixo)

    def __str__(self):
        return f"{self.prefixo.value}-{self.sufixo}"

    @validator("sufixo")
    def valida_sufixo(cls, v: str):
        if len(v) != 3:
            raise ValueError("O sufixo deve ter 3 letras")
        if not v.isupper():
            raise ValueError("O sufixo deve ser uppercase")
        if not v.isalpha():
            raise ValueError("O sufixo deve ser composto somente por letras")
        return v


class RegistroDePassagem(BaseModel):
    number: int

    def __init__(self, number: int):
        super().__init__(number=number)

    @validator("numero")
    def valida_numero(self, numero: int):
        if numero < 0:
            raise ValueError("Numero deve ser não negativo")
        return numero

    def __str__(self):
        return f"{self.number}"


class RegistroDeViagem(BaseModel):
    prefixo: str
    numero: int

    def __init__(self, prefixo: str, numero: int):
        super().__init__(prefixo=prefixo, numero=numero)

    def __str__(self):
        return f"{self.prefixo}{self.numero:0>4}"

    @validator("prefixo")
    def valida_prefixo(self, v: str):
        if len(v) != 2:
            raise ValueError("O prefixo deve ter dois caracteres")
        if not v.isupper():
            raise ValueError("O prefixo deve ser uppercase")
        if not v.isalpha():
            raise ValueError("O prefixo deve ser feito de letras")
        return v

    @validator("numero")
    def valida_numero(self, v: int):
        if v < 0:
            raise ValueError("O numero é negativo")
        if v > 9999:
            raise ValueError("O numero é muito grande")
        return v


class SiglaAeroporto(BaseModel):
    sigla: str

    def __init__(self, sigla: str):
        super().__init__(sigla=sigla)

    def __str__(self):
        return self.sigla

    @validator("sigla")
    def valida_sigla(self, v: str):
        if len(v) != 3:
            raise ValueError("A sigla deve ter 3 caracteres")
        if not v.isupper():
            raise ValueError("A sigla deve ser uppercase")
        if not v.isalpha():
            raise ValueError("A sigla deve ser feita de caracteres")
        return v


class RG(BaseModel):
    rg: str

    def __init__(self, rg: str):
        super().__init__(rg=rg)

    @validator("rg")
    def valida_rg(self, rg: str):
        estado = rg[2:]
        numeros = rg[:2]
        if not hasattr(Estado, estado):
            raise ValueError("Estado invalido")
        if not numeros.isdigit():
            raise ValueError("Resto do rg não é numero")
        if not len(numeros) == 9:
            raise ValueError("Não são 9 numeros")
        digitos = list(map(int, numeros))
        weights = [2, 3, 4, 5, 6, 7, 8, 9]
        sum_ = sum(d * w for d, w in zip(digitos[:-1], weights))
        dv = (sum_ % 11)
        if dv == 0:
            dv = 11
        if dv != digitos[-1]:
            raise ValueError('Numero de RG invalido')
        return rg

    def __str__(self):
        return self.rg


class Passaporte(BaseModel):
    passaporte: str

    def __init__(self, passaporte: str):
        super().__init__(passaporte=passaporte)

    @validator("passaporte")
    def valida_passaporte(self, passaporte: str):
        if not passaporte.isalnum():
            raise ValueError('Um passaporte deve ser alfanumerico')
        if len(passaporte) != 9:
            raise ValueError('Um passaporte deve ter 9 caracteres')
        if not passaporte.startswith('A'):
            raise ValueError('Um passaporte deve começar com um A')
        return passaporte

    def __str__(self):
        return self.passaporte


class DocumentoCliente(BaseModel):
    passaporte: Optional[Passaporte] = None
    rg: Optional[RG] = None

    def __init__(self, **kwargs):
        if "rg" not in kwargs and "passaporte" not in kwargs:
            raise ValueError("Ou um passaporte ou um rg devem ser especificados")
        super().__init__(**kwargs)

    def documento(self) -> Passaporte | RG:
        return self.passaporte or self.rg

    def __str__(self):
        return f"{self.documento()}"


class GeradorDeRegistroDeViagem:
    ultimo_id: int

    def __init__(self, ultimo_id: Optional[int]):
        self.ultimo_id = ultimo_id or -1

    def gerar(self) -> RegistroDeViagem:
        self.ultimo_id += 1
        id = self.ultimo_id
        numero = id % 10000
        prefixo = chr(ord('A') + (id - 1) // 26) + chr(ord('A') + (id - 1) % 26)
        return RegistroDeViagem(prefixo, numero)


class GeradorDeRegistroDePassagem:
    ultimo_id: int

    def __init__(self, ultimo_id: Optional[int]):
        self.ultimo_id = ultimo_id or -1

    def gerar(self):
        self.ultimo_id += 1
        id = self.ultimo_id
        return RegistroDePassagem(id)


class Classe(str, Enum):
    EXECUTIVA = "executiva"
    STANDARD = "standard"

    @staticmethod
    def prefixo(classe: "Classe"):
        match classe:
            case Classe.EXECUTIVA:
                return "E"
            case Classe.STANDARD:
                return "S"


class CodigoDoAssento(BaseModel):
    classe: Classe
    coluna: str
    fileira: int

    def __init__(self,
                 classe: Classe,
                 coluna: str,
                 fileira: int):
        super().__init__(classe=classe, coluna=coluna, fileira=fileira)

    def __str__(self):
        return f"{Classe.prefixo(self.classe)}{self.coluna}{self.fileira:0>2}"


class GeradorDeCodigoDoAssento:
    def __init__(self, passenger_count: int, executive_ratio: float = 0.2):
        self.passenger_count = passenger_count
        self.executive_count = int(passenger_count * executive_ratio)
        self.standard_count = passenger_count - self.executive_count
        self.seats_per_row = self._calculate_seats_per_row()  # calculate based on passenger count
        self.rows_executive = ceil(self.executive_count / self.seats_per_row)
        self.rows_standard = ceil(self.standard_count / self.seats_per_row)
        self.current_index = 1  # Starting index for seat IDs

    def _calculate_seats_per_row(self) -> int:
        """
        Calculates the number of seats per row based on the passenger count.
        Assumes a 3-4-3 configuration for standard seats and a 2-2 configuration for executive seats.
        """
        standard_seats_per_row = 10  # starting guess for a large airplane
        executive_seats_per_row = 4  # starting guess for a large airplane
        while True:
            standard_rows = ceil(self.standard_count / standard_seats_per_row)
            executive_rows = ceil(self.executive_count / executive_seats_per_row)
            total_rows = standard_rows + executive_rows
            if total_rows <= 80:  # upper limit for a small airplane
                return standard_seats_per_row
            else:
                standard_seats_per_row -= 1
                executive_seats_per_row -= 1

    def gerar(self) -> CodigoDoAssento:
        """
        Generates the next seat ID and returns it along with the passenger count.

        Returns:
            Tuple containing the seat ID and the number of passengers left to assign seats to.
        """
        if self.current_index <= self.executive_count:
            row = (self.current_index - 1) // self.seats_per_row + 1
            coluna = (self.current_index - 1) % self.seats_per_row + 1
            classe = Classe.EXECUTIVA
        else:
            row = (self.current_index - self.executive_count - 1) // self.seats_per_row + 1
            coluna = (self.current_index - self.executive_count - 1) % self.seats_per_row + 1
            classe = Classe.STANDARD
        fileira = f"{chr(ord('A') + coluna - 1)}"
        self.current_index += 1
        passengers_left = self.passenger_count - (self.current_index - 1)
        return CodigoDoAssento(classe, fileira, coluna)

    def gerar_todos(self) -> list[CodigoDoAssento]:
        if self.current_index != 1:
            raise ValueError("O gerador deve iniciar vazio")
        codigos = []
        while self.passenger_count - (self.current_index - 1) != 0:
            codigos.append(self.gerar())
        return codigos
