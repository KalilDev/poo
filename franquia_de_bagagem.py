from pydantic import BaseModel, validator


class FranquiaDeBagagem(BaseModel):
    peso: float

    def __init__(self, peso: float):
        super().__init__(peso=peso)

    @validator("peso")
    def validar_peso(self, peso: float):
        if peso > 23.0:
            raise ValueError("O peso máximo de uma franquia é 23kg")
        return peso


class FranquiasDeBagagem(BaseModel):
    franquias: list[FranquiaDeBagagem]

    def __init__(self, franquias: list[FranquiaDeBagagem]):
        super().__init__(franquias=franquias)

    @validator("franquias")
    def validar_franquias(self, franquias: list[FranquiaDeBagagem]):
        if len(franquias) > 3:
            raise ValueError("No maximo três franquias são suportadas")
        return franquias

    def carga(self) -> float:
        carga = 0
        for franquia in self.franquias:
            carga += franquia.peso
        return carga
