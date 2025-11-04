from sqlalchemy import Column, Integer, Float, ForeignKey
from models.account import Account

class CheckingAccount(Account):
    __tablename__ = "checking_accounts"

    id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)
    limit = Column(Float, default=0.0)

    __mapper_args__ = {
        "polymorphic_identity": "checking_account",
    }

    def set_limit(self, value: float):
        """Define o limite do cheque especial"""
        if value < 0:
            raise ValueError("O limite não pode ser negativo.")
        self.limit = value
        return f"Limite definido para R${value:.2f}"

    def withdraw(self, value: float):
        """Realiza saque considerando o limite do cheque especial"""
        if value <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        
        disponivel = (self.balance or 0.0) + (self.limit or 0.0)
        if value > disponivel:
            raise ValueError(f"Saldo insuficiente. Disponível para saque: R${disponivel:.2f}")
        
        self.balance -= value
        return f"Saque de R${value:.2f} realizado. Saldo: R${self.balance:.2f}"

    def get_available_balance(self):
        """Retorna o saldo disponível (saldo + limite)"""
        return (self.balance or 0.0) + (self.limit or 0.0)

    def __repr__(self):
        return f"<CheckingAccount {self.number} - Saldo: R${self.balance:.2f} - Limite: R${self.limit:.2f}>"