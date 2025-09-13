import datetime

from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.sessions import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    match_score = Column(Float, nullable=False)
    missing_skills = Column(JSON, nullable=False)
    recommended_courses = Column(JSON, nullable=False)
    project_suggestions = Column(JSON, nullable=False)
    full_analysis_text = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="analysis_results")