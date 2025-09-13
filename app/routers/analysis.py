from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

# Make sure this import is correct
from ..schemas.analysis import AnalysisResult, AnalysisResultCreate
from .. import models
from ..db.sessions import get_db  # <-- CORRECTED LINE
from ..services import ai_service, auth_service
from ..utils import file_parser

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)

@router.post("/", response_model=AnalysisResult, status_code=status.HTTP_201_CREATED)
async def analyze_resume_and_jd(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
    current_user: models.users = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyzes a resume against a job description. This endpoint is protected.
    """
    try:
        # 1. Parse file content
        resume_content = await resume.read()
        jd_content = await job_description.read()
        resume_text = await file_parser.parse_file_content(resume_content, resume.filename)
        jd_text = await file_parser.parse_file_content(jd_content, job_description.filename)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # 2. Get analysis from the AI Service
    try:
        ai_output = await ai_service.get_analysis_from_gemini(resume_text, jd_text)
        analysis_data = AnalysisResultCreate(**ai_output)
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"AI service failed: {e}")
        
    # 3. Store the result in PostgreSQL
    db_analysis = models.AnalysisResult(
        **analysis_data.model_dump(),
        owner_id=current_user.id
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return db_analysis