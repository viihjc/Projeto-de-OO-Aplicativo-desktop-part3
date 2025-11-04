from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///banco.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()