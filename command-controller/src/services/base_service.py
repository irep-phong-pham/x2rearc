from abc import ABC
from src.daos import FactoryInterface, ConcreteFactory


class BaseService(ABC):
    def __init__(self, dao_factory: FactoryInterface = None):
        if dao_factory is None:
            self.dao_factory = ConcreteFactory()
        else:
            self.dao_factory = dao_factory
