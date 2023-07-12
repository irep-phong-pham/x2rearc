from src.database import Database
from .base_dao_interface import BaseDaoInterface
import logging

logger = logging.getLogger(__name__)


class BaseDao(BaseDaoInterface):
    def __init__(self, *args, **kwargs):
        self.db = Database()
        if 'table_name' in kwargs:
            self.table_name = kwargs['table_name']
        else:
            self.table_name = None
