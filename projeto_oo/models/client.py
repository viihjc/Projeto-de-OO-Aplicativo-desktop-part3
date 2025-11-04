from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)  

    accounts = relationship("Account", back_populates="client", cascade="all, delete-orphan")

    def __init__(self, name):
        if not name.replace(" ", "").isalpha():
            raise ValueError("Nome deve conter apenas letras e espaços.")
        self.name = name

    def __repr__(self):
        return f"<Client {self.name}>"