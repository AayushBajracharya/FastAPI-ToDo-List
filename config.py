import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# import os
# from dotenv import load_dotenv
# from sqlmodel import create_engine, Session

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL, echo=True)

# def get_session():
#     with Session(engine) as session:
#         yield session
