# app/models/user_tables.py

from sqlalchemy import Column, Integer, String
from app.config.database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
# from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True, nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(70), nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
