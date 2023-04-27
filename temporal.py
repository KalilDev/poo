import datetime

from pydantic import BaseModel, validator, Field


class Duracao(BaseModel):
    dias: int = Field(0)
    segundos: int = Field(0)
    @staticmethod
    def um_dia():
        return Duracao(dias=1)
    @staticmethod
    def um_segundo():
        return Duracao(segundos=1)

    @staticmethod
    def meia_hora():
        minuto = 60
        hora = 60
        return Duracao(segundos=minuto * hora / 2)

    @staticmethod
    def from_timedelta(timedelta: datetime.timedelta) -> "Duracao":
        return Duracao(dias=timedelta.days, segundos=timedelta.seconds)

    def to_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(days=self.dias, seconds=self.segundos)

    def __sub__(self, other: "Duracao"):
        return Duracao.from_timedelta(self.to_timedelta() - other.to_timedelta())

    def __add__(self, other: "Duracao"):
        return Duracao.from_timedelta(self.to_timedelta() + other.to_timedelta())

    def __mul__(self, other: float):
        return Duracao.from_timedelta(self.to_timedelta() * other)

    def __gt__(self, other: "Duracao"):
        return self.to_timedelta() > other.to_timedelta()

class DiaDaSemana(str, Enum):
    SEGUNDA = "segunda"
    TERCA = "terca"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SEXTA = "sexta"
    SABADO = "sabado"
    DOMINGO = "domingo"

    @staticmethod
    def from_weekday(weekday: int):
        match weekday:
            case 0:
                return DiaDaSemana.SEGUNDA
            case 1:
                return DiaDaSemana.TERCA
            case 2:
                return DiaDaSemana.QUARTA
            case 3:
                return DiaDaSemana.QUINTA
            case 4:
                return DiaDaSemana.SEXTA
            case 5:
                return DiaDaSemana.SABADO
            case 6:
                return DiaDaSemana.DOMINGO


class Data(BaseModel):
    dia_da_semana: DiaDaSemana
    dia: int
    mes: int
    ano: int

    @validator('dia')
    def validate_dia(cls, v):
        if not 1 <= v <= 31:
            raise ValueError('Day must be between 1 and 31')
        return v

    @validator('mes')
    def validate_mes(cls, v):
        if not 1 <= v <= 12:
            raise ValueError('Month must be between 1 and 12')
        return v

    @validator('ano')
    def validate_ano(cls, v):
        if v < 0:
            raise ValueError("Year must not be negative")
        return v

    @staticmethod
    def from_datetime(datetime: datetime.datetime):
        return Data(dia=datetime.day, mes=datetime.month, ano=datetime.year,
                    dia_da_semana=DiaDaSemana.from_weekday(datetime.weekday()))

    def com_tempo(self, tempo: "Tempo") -> "DataTempo":
        return DataTempo(data=self, tempo=tempo)

    @staticmethod
    def now() -> "Data":
        return Data.from_datetime(datetime.datetime.now())

    def to_datetime(self) -> datetime.datetime:
        return datetime.datetime(day=self.dia, month=self.mes, year=self.ano)

    def __sub__(self, other: "Data") -> Duracao:
        return Duracao.from_timedelta(self.to_datetime() - other.to_datetime())

    def __add__(self, other: Duracao):
        return Data.from_datetime(self.to_datetime() + other.to_timedelta())


class Tempo(BaseModel):
    hora: int
    minuto: int
    segundo: int

    @validator('hora')
    def validate_hora(cls, v):
        if not 0 <= v <= 23:
            raise ValueError('Hour must be between 0 and 23')
        return v

    @validator('minuto')
    def validate_minuto(cls, v):
        if not 0 <= v <= 59:
            raise ValueError('Minuto must be between 0 and 59')
        return v

    @validator('segundo')
    def validate_segundo(cls, v):
        if not 0 <= v <= 59:
            raise ValueError('Segundo must be between 0 and 59')
        return v

    @staticmethod
    def from_datetime(datetime: datetime.datetime) -> "Tempo":
        return Tempo(hora=datetime.hour, minuto=datetime.minute, segundo=datetime.second)

    def to_datetime(self, date: datetime.datetime = datetime.datetime.now()) -> datetime.datetime:
        return datetime.datetime(hour=self.hora, minute=self.minuto, second=self.segundo, day=date.day,
                                 month=date.month, year=date.year)

    @staticmethod
    def now() -> "Tempo":
        return Tempo.from_datetime(datetime.datetime.now())

    def com_data(self, data: Data) -> "DataTempo":
        return DataTempo(data=data, tempo=self)

    def __sub__(self, other: "Tempo") -> Duracao:
        return Duracao.from_timedelta(self.to_datetime() - other.to_datetime())

    def __add__(self, other: Duracao):
        return DataTempo.from_datetime(self.to_datetime() + other.to_timedelta())


class DataTempo(BaseModel):
    data: Data
    tempo: Tempo

    @staticmethod
    def from_datetime(datetime: datetime.datetime) -> "DataTempo":
        return DataTempo(data=Data(dia=datetime.day, mes=datetime.day, ano=datetime.year),
                         tempo=Tempo(hora=datetime.hour, minuto=datetime.minute, segundo=datetime.second))

    def to_datetime(self):
        return datetime.datetime(day=self.data.dia, month=self.data.mes, year=self.data.ano, hour=self.tempo.hora,
                                 minute=self.tempo.minuto, second=self.tempo.segundo)

    @staticmethod
    def now() -> "DataTempo":
        return DataTempo.from_datetime(datetime.datetime.now())

    def __sub__(self, other: "DataTempo"):
        return Duracao.from_timedelta(self.to_datetime() - other.to_datetime())

    def __add__(self, other: Duracao):
        return DataTempo.from_datetime(self.to_datetime() + other.to_timedelta())
