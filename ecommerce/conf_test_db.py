from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ecommerce.db import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:secretpassword@0.0.0.0:5432/test_database"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
