from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ControlBD:
    def __init__(self):
        database_dir = os.path.abspath(os.path.dirname(__file__))
        database_uri = f'sqlite:///{database_dir}/base.db?check_same_thread=False'
        self.Session = sessionmaker()
        self.engine = create_engine(database_uri)
        self.session = self.Session(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_position(self, name, price, description='', count=0):
        self.session.add(Praise(name=name, count=count, price=price, description=description))
        self.session.commit()

    def commit(self):
        self.session.commit()

    def find(self, name=None, id=None):
        if not (name or id):
            raise Exception('Не указано имя или id')
        if name:
            tolk = (self.session.query(Praise).filter(
                Praise.name == name
            ).first())
        else:
            tolk = (self.session.query(Praise).filter(
                Praise.id == id
            ).first())
        return tolk

    def del_position(self, name=None, id=None):
        self.session.delete(self.find(name=name, id=id))
        self.session.commit()

    def remove_position(self, new_name, new_count, name=None, id=None):
        tolk = self.find(name=name, id=id)
        tolk.name = new_name
        tolk.count = new_count if new_count != -1 else tolk.count
        self.session.commit()

    def remove_count(self, count, name=None, id=None):
        tolk = self.find(name=name, id=id)
        if isinstance(count, int):
            tolk.count = count
        else:
            tolk.count += 1 if count == '+' else -1
        self.session.commit()

    def get(self):
        return self.session.query(Praise).all()

    def close(self):
        self.session.commit()
        self.session.close()

class Praise(Base):
    __tablename__ = 'skl'

    id = Column(Integer(), autoincrement="auto", primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(150))
    count = Column(Integer(), nullable=False)
    price = Column(Integer(), nullable=False)


    def __repr__(self):
        return f'<Student name="{self.name}" count={self.count}>'

if __name__ == '__main__':
    contr = ControlBD()
    print(contr.find(9))