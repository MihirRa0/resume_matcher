from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.orm import relationship
from app.db.sessions import Base


class User(Base):
    __tablename__ = "users"
    id =  Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index=True,nullable= False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    analysis_results = relationship("AnalysisResult",back_populates="owner")
    