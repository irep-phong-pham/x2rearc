from __future__ import annotations
from threading import Lock
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class SingletonMeta(type):
    _instance = None
    _lock: Lock = Lock()
    """
    Lock object that will be used to synchronize threads during
    first access to the Singleton.
    """
    def __call__(cls, *args, **kwargs):
        # sync between threads
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Database(metaclass=SingletonMeta):
    def __init__(self, app=None, uri=None):
        try:
            pool_recycle = 3600
            if not uri:
                if app:
                    uri = app.config.get('SQLALCHEMY_DATABASE_URI')
                    pool_recycle = app.config.get('SQLALCHEMY_POOL_RECYCLE',
                                                  3600)
                elif os.environ.get('SQLALCHEMY_DATABASE_URI'):
                    uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
                    pool_recycle = os.environ.get('SQLALCHEMY_POOL_RECYCLE',
                                                  3600)
            if not uri:
                raise ValueError('Should be set SQLALCHEMY_DATABASE_URI uri !')
            print('INIT: Connecting!')
            self.engine = sqlalchemy.create_engine(uri,
                                                   pool_recycle=pool_recycle)

            self.Session = scoped_session(sessionmaker(bind=self.engine))
            print('SUCCESS: Connection established to {}\n'.format(uri))
        except Exception as e:
            print(
                "ERROR: Unexpected error: Could not connect to MySQL instance."
            )
            raise e

    @staticmethod
    def to_dict(result_proxy):
        return [dict(r) for r in result_proxy]
