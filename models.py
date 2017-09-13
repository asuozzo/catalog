from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from wtforms import Form, BooleanField, StringField, PasswordField, validators

Base = declarative_base()

class RegistrationForm(Form):
    username = StringField('Username', [
        validators.Length(min=3, max=20),
        validators.DataRequired()
        ])
    email = StringField("Email Address", [
        validators.Length(min=6,max=35),
        validators.DataRequired()
        ])
    password=PasswordField("Password", [validators.DataRequired()])

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    genre = Column(String)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'id' : self.id,
        'title' : self.title,
        'description' : self.description,
        'author' : self.author,
        'genre' : self.genre
            }


engine = create_engine('sqlite:///library.db')


Base.metadata.create_all(engine)