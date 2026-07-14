from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine

DB_URL ="mysql+pymysql://root:tuyen111273@localhost:3306/student_management"

engine = create_engine(DB_URL)

Base = declarative_base()

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
    expire_on_commit=False
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()