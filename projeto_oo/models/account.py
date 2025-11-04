from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String, unique=True, index=True, nullable=True) 
    balance = Column(Float, default=0.0)
    type = Column(String(50))
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("Client", back_populates="accounts")
    extratos = relationship("Extrato", back_populates="account", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "account",
        "polymorphic_on": type
    }

    def deposit(self, value: float):
        if value <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self.balance += value
        return f"Depósito de R${value:.2f} realizado. Saldo: R${self.balance:.2f}"

    def withdraw(self, value: float):
        if value <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if value > self.balance:
            raise ValueError(f"Saldo insuficiente. Saldo atual: R${self.balance:.2f}")
        self.balance -= value
        return f"Saque de R${value:.2f} realizado. Saldo: R${self.balance:.2f}"

    def __repr__(self):
        return f"<Account {self.number} - Saldo: R${self.balance:.2f}>"