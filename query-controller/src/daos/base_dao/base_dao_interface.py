from abc import ABC, abstractmethod


class BaseDaoInterface(ABC):
    def bulk_insert_mapping(self, data: dict, table_name: str = None):
        raise NotImplementedError
