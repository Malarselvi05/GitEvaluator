from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database, auth, worker
from .services.github_service import GitHubService
from .services.ai_service import AIService

app = FastAPI(title="GitHub Project Evaluator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the GitHub Project Evaluator API"}

@app.post("/analyze", response_model=schemas.User)
async def analyze_profile(
    username: str, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    # Check if user exists or create
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        # For MVP, we'd normally get this from GitHub OAuth
        user = models.User(username=username, github_id=0) # Placeholder ID
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Trigger background analysis
    worker.analyze_profile_task.delay(str(user.id), username, "placeholder_token") # Token should come from OAuth
    
    return user

@app.get("/profile/{username}", response_model=schemas.ProfileSummary)
async def get_profile(username: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Mock summary for now
    return {
        "username": user.username,
        "overall_score": 76.5,
        "grade": "B+",
        "repos_analyzed": 3,
        "top_repos": [],
        "recent_analyses": [],
        "recruiter_verdict": "Shortlist"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
