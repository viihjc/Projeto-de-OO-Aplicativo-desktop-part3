from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Extrato(Base):
    __tablename__ = "extratos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)

    account = relationship("Account", back_populates="extratos")

    def __repr__(self):
        return f"[{self.date.strftime('%d/%m/%Y %H:%M')}] {self.description}"