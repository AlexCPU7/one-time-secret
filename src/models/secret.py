from sqlalchemy import Column, String, Text, Integer

from database import Base


class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True)
    secret_key = Column(String(36), nullable=True)
    hash_secret_phrase = Column(String(64), nullable=True)
    hash_message = Column(Text, nullable=True)
