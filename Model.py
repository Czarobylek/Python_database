from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, String, Float, Date
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('postgresql://postgres:PostgersSQL123@localhost/Company_2', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Department(Base):
    __tablename__ = 'Department'
    Name = Column(String(20), index=True, primary_key=True)
    address = Column(String(40))
    phone = Column(String(20))
    email = Column(String(40))
    WWW = Column(String(200))
    description = Column(String(250))
    fk_manager = Column(String(20), ForeignKey('AppUser.userName'))
    users = relationship('AppUser', backref='department', foreign_keys='Department.fk_manager')


class AppUser(Base):
    __tablename__ = 'AppUser'
    userName = Column(String(20), index = True, primary_key = True)
    password = Column(String(40))
    firstName = Column(String(20))
    lastName = Column(String(40))
    description = Column(String(250))
    payment = Column(Float)
    bonus = Column(Float)
    dateOfPayment = Column(Date)
    fk_department = Column(String(20), ForeignKey('Department.Name'))
    #department = relationship('Department', back_populates='users', foreign_keys='AppUser.fk_department')
    manager = relationship('Department', uselist=False, foreign_keys='AppUser.fk_department')

Base.metadata.create_all(engine)

#asas
