import os

from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_PORT")
TEST_DATABASE_NAME = os.getenv("TEST_DATABASE_NAME")