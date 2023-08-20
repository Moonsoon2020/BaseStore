from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Boolean
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin


Base = declarative_base()

class ControlBD:
    def __init__(self):
        database_dir = os.path.abspath(os.path.dirname(__file__))
        database_uri = f'sqlite:///{database_dir}/base.db?check_same_thread=False'
        self.Session = sessionmaker()
        self.engine = create_engine(database_uri)
        self.session = self.Session(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_product(self, name, price, description='', count=0):
        self.session.add(Product(name=name, count=count, price=price, description=description))
        self.session.commit()

    def commit(self):
        self.session.commit()

    def find_product(self, name=None, id=None):
        if not (name or id):
            raise Exception('Не указано имя или id')
        if name:
            tolk = (self.session.query(Product).filter(
                Product.name == name
            ).first())
        else:
            tolk = (self.session.query(Product).filter(
                Product.id == id
            ).first())
        return tolk

    def del_product(self, name=None, id=None):
        self.session.delete(self.find_product(name=name, id=id))
        self.session.commit()

    def remove_count(self, count, name=None, id=None):
        tolk = self.find_product(name=name, id=id)
        if isinstance(count, int):
            tolk.count = count
        else:
            tolk.count += 1 if count == '+' else -1
        self.session.commit()

    def get(self):
        return self.session.query(Product).all()

    def add_position(self, name, price, recept, description=''):
        self.session.add(Prise(name=name, description=description, price=price, recept=recept))
        self.session.commit()

    def del_position(self, name=None, id=None):
        self.session.delete(self.find_position(name=name, id=id))
        self.session.commit()

    def remove_position(self, new_name, new_count, name=None, id=None):
        tolk = self.find_position(name=name, id=id)
        tolk.name = new_name
        tolk.count = new_count if new_count != -1 else tolk.count
        self.session.commit()

    def find_position(self, name=None, id=None):
        if not (name or id):
            raise Exception('Не указано имя или id')
        if name:
            tolk = (self.session.query(Prise).filter(
                Prise.name == name
            ).first())
        else:
            tolk = (self.session.query(Prise).filter(
                Prise.id == id
            ).first())
        return tolk

    def close(self):
        self.session.commit()
        self.session.close()

    def load_user(self, user_id):
        return self.session.query(User).get(int(user_id))

    def user_get_p(self, username):
        return self.session.query(User).filter_by(username=username).first()

    def add_user(self, username, password):
        new_user = User(username=username, password=password, ok=False)
        self.session.add(new_user)
        self.session.commit()

    def get_user(self):
        return self.session.query(User).all()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer(), autoincrement="auto", primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(150))
    count = Column(Integer(), nullable=False)
    price = Column(Integer(), nullable=False)


    def __repr__(self):
        return f'<Student name="{self.name}" count={self.count}>'

class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True, autoincrement="auto")
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    ok = Column(Boolean(), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Prise(Base):
    __tablename__ = 'prise'

    id = Column(Integer(), primary_key=True, autoincrement="auto")
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(50))
    price = Column(Integer(), nullable=False)
    recept = Column(String(500), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


if __name__ == '__main__':
    contr = ControlBD()
