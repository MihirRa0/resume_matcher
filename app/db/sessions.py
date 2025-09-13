from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


#? establishes the actual connection pool to your PostgreSQL server.
engine = create_engine(settings.DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db=SessionLocal()
    try :
        yield db
    finally:
        db.close()


'''
SessionLocal: This is not a database session itself, but a factory that creates sessions when requested. We configure it with:
autocommit=False & autoflush=False: This gives us full control. Data is only saved to the database when we explicitly call db.commit().

bind=engine: This tells the sessions created by this factory that they should use our engine to communicate.'''