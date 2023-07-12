from .task_dao_interface import TaskDAOInterface
from ..base_dao import BaseDao


class TaskDAO(BaseDao, TaskDAOInterface):
    def __init__(self):
        BaseDao.__init__(self)

    def get(self, id):
        session = self.db.Session()
        try:
            query = """
            SELECT id, name, description
            FROM T_TASKS
            WHERE id=:id
            AND valid_flag=1;
            """
            res_p = session.execute(query, {'id': id})
            print(res_p)
            res = self.db.to_dict(res_p)
            if res:
                return res[0]
            return None
        finally:
            session.close()

    def get_all(self):
        return []
