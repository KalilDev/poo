from passageiro import Passageiro
from franquia_de_bagagem import FranquiasDeBagagem


class CalculoTarifaStrategy:
    def calcula(self, franquias: FranquiasDeBagagem) -> float:
        pass


class PassageiroComumCalculoTarifaStrategy(CalculoTarifaStrategy):
    tarifa: float
    tarifa_franquia: float

    def __init__(self,
                 tarifa: float,
                 tarifa_franquia: float, ):
        self.tarifa = tarifa
        self.tarifa_franquia = tarifa_franquia

    def calcula(self, franquias: FranquiasDeBagagem) -> float:
        return self.tarifa * len(franquias.franquias) * self.tarifa_franquia


class PassageiroVipCalculoTarifaStrategy(CalculoTarifaStrategy):
    tarifa: float
    tarifa_franquia: float

    def __init__(self,
                 tarifa: float,
                 tarifa_franquia: float, ):
        self.tarifa = tarifa
        self.tarifa_franquia = tarifa_franquia

    def calcula(self, franquias: FranquiasDeBagagem) -> float:
        franquias_a_serem_pagas = len(franquias.franquias)
        if franquias_a_serem_pagas == 0:
            return self.tarifa
        franquias_a_serem_pagas -= 1

        return self.tarifa * franquias_a_serem_pagas * self.tarifa_franquia / 2

def calculo_tarifa_strategy_for(cliente_vip: bool, tarifa: float, tarifa_franquia: float):
    if cliente_vip:
        return PassageiroVipCalculoTarifaStrategy(tarifa, tarifa_franquia)
    return PassageiroComumCalculoTarifaStrategy(tarifa, tarifa_franquia)
