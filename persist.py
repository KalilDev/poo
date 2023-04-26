from typing import Type

from container import Container


class Persist:
    filename = None
    index = None

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 1:
            self.index = args[0]
        else:
            raise Exception('Error ao instanciar objeto da classe Persist - Número de parâmetros incorreto.')

    def load(self, obj):
        class_vars = vars(obj.__class__)
        for name, value in class_vars.items():
            print(f"{name} : {value}")
            setattr(self, name, value)

    def save(self):
        if self.index is not None:
            self.edit()
        else:
            self.insert()

    def insert(self):
        container = Container.get_instance(self.__class__.get_filename())
        container.add_object(self)
        container.persist()

    def edit(self):
        container = Container.get_instance(self.__class__.get_filename())
        container.edit_object(self.index, self)
        container.persist()

    @staticmethod
    def get_records_by_field(field, value, called_class: Type["Persist"]):
        container = Container.get_instance(called_class.get_filename())
        objs = container.get_objects()
        match_objects = []

        for obj in objs:
            if getattr(obj, field) == value:
                match_objects.append(obj)

        return match_objects

    @staticmethod
    def get_records(called_class: Type["Persist"]):
        container = Container.get_instance(called_class.get_filename())
        objs = container.get_objects()
        return objs

    def set_index(self, index):
        self.index = index

class Funcionario(Persist):
    nome: str
    cpf: str
    local_filename: str = "funcionario.txt"

    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf = cpf
        super().__init__()

    @staticmethod
    def get_records_by_field(field, value):
        return Persist.get_records_by_field(field, value, Funcionario)

    @staticmethod
    def get_records():
        return Persist.get_records(Funcionario)

    @staticmethod
    def get_filename():
        return Funcionario.local_filename