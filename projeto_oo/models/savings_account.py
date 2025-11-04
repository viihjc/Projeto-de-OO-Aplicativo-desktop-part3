from sqlalchemy import Column, Integer, ForeignKey
from models.account import Account

class SavingsAccount(Account):
    __tablename__ = "savings_accounts"

    id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "savings_account",
    }