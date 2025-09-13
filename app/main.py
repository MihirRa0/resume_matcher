from fastapi import FastAPI
from .routers import auth, analysis # <-- Import the new router

app = FastAPI(
    title="Smart Resume Matcher API",
    description="An API to match resumes with job descriptions and provide skill gap analysis.",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(analysis.router) # <-- Add the new router to the app

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Smart Resume Matcher API!"}