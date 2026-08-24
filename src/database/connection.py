from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parents[2]

# Database path
DATABASE_PATH = BASE_DIR / "data" / "blood_bank.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)