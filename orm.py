#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Time, Float
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine("mysql+pymysql://root:123@localhost:3306/twitter", pool_recycle=3600)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = DBSession()
    try:
        yield session
        #session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class Cailian(Base):
    __tablename__ = "cailian"
    id = Column(Integer, primary_key=True)
    content = Column(String(10240))
    ctime = Column(Float)
    created_at = Column(Float)