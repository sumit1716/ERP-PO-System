from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Yahan 'your_password' ki jagah apna pgAdmin wala password dalo
DATABASE_URL = "postgresql://postgres:Sumit@localhost:5432/erp_system"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()