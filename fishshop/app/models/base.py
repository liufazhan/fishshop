from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy,BaseQuery
from sqlalchemy import Column,Integer,SmallInteger
from datetime import datetime


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    # 重写filter_by方法
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status']=1
        return super(Query,self).filter_by(**kwargs)


db=SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 让sqlalchemy 不去创建表，而把它当做一个基类可以使用以下
    __abstract__=True
    create_time=Column('create_time',Integer)
    def __init__(self):
        # 获取当前时间，以时间戳的形式返回
        self.create_time=int(datetime.now().timestamp())
    status=Column(SmallInteger,default=1)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None