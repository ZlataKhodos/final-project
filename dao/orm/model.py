from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

Base = declarative_base()

class order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False)
    date = Column(Date)
    criteria = Column(String(20), nullable=False)
    value = Column(String(40), nullable=False)

class performer(Base):
    __tablename__='performer'
    __table_args__ = (
        UniqueConstraint('name'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    album = relationship("album", back_populates="performer")

class album(Base):
    __tablename__='album'
    __table_args__ = (
        UniqueConstraint('title', 'performer_id'),
    )
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    performer_id = Column(Integer, ForeignKey('performer.id'))
    performer = relationship("performer", back_populates="album")
    melody = relationship("melody", back_populates="album")

class student(UserMixin, Base):
    __tablename__ = 'student'
    __table_args__ = (
        UniqueConstraint('username'),
    )
    id = Column(Integer, primary_key=True)
    faculty = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    name = Column(String(20), nullable=False)
    username = Column(String(40), nullable=False)
    password = Column(String(300), nullable=False)
    wish = relationship("wish", back_populates="student")

class genre(Base):
    __tablename__ = 'genre'
    __table_args__ = (
        UniqueConstraint('name'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    psychotype = Column(String(25))
    melody = relationship("melody", back_populates="genre")

class melody(Base):
    __tablename__ = 'melody'
    __table_args__ = (
        UniqueConstraint('title', 'singer', 'release_date', 'melody_genre', 'album_id'),
    )
    id = Column(Integer, primary_key=True)
    title = Column(String(15))
    singer = Column(String(25))
    release_date = Column(Date)
    melody_genre = Column(Integer, ForeignKey('genre.id'))
    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship("album", back_populates="melody")
    wish = relationship("wish", back_populates="melody")
    genre = relationship("genre", back_populates="melody")

class wish(Base):
    __tablename__ = 'wish'
    __table_args__ = (
        UniqueConstraint('student_id', 'wish_date', 'wish_criteria'),
    )
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    wish_date = Column(Date)
    wish_criteria = Column(String(15), nullable=False)
    melody_id = Column(Integer, ForeignKey('melody.id'))
    melody = relationship("melody", back_populates="wish")
    student = relationship("student", back_populates="wish")