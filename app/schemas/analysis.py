from typing import List
from pydantic import BaseModel,Field
import datetime


class AnalysisResultBase(BaseModel):
    match_score: float = Field(..., ge=0, le=100)
    missing_skills: List[str]
    recommended_courses: List[str]
    project_suggestions: List[str]
    full_analysis_text: str | None = None  #sets a sought of optional(default value agar nhi aaaya data toh )

#!AnalysisResultCreate is what we'll use to validate the data coming from the Gemini API.
class AnalysisResultCreate(AnalysisResultBase):
    pass


#?AnalysisResult is the full object we'll return from our API after it's been saved to the database.
class AnalysisResult(AnalysisResultBase):
    id: int
    owner_id: int
    created_at: datetime.datetime

    class Config:
        from_attribues = True