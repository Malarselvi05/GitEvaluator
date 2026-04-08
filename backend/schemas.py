from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# User Schemas
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    plan: str = "free"

class UserCreate(UserBase):
    github_id: int
    access_token: str

class User(UserBase):
    id: UUID
    created_at: datetime
    last_analyzed: Optional[datetime] = None

    class Config:
        from_attributes = True

# Repository Schemas
class RepositoryBase(BaseModel):
    github_id: int
    name: str
    full_name: str
    description: Optional[str] = None
    language: Optional[str] = None
    topics: List[str] = []
    stars: int = 0
    forks: int = 0
    is_fork: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    pushed_at: Optional[datetime] = None

class Repository(RepositoryBase):
    id: UUID
    user_id: UUID
    fetched_at: datetime

    class Config:
        from_attributes = True

# Analysis Schemas
class AnalysisResultSchema(BaseModel):
    code_quality_score: int
    impact_score: int
    innovation_score: int
    completeness_score: int
    relevance_score: int
    composite_score: float
    complexity_tier: str
    is_commodity_project: bool
    resume_worthy: bool
    one_line_summary: str
    ai_reasoning: Dict[str, Any]
    improvement_actions: List[Dict[str, Any]]
    resume_bullet: Optional[str] = None
    generated_readme: Optional[str] = None
    linkedin_description: Optional[str] = None

class AnalysisSchema(AnalysisResultSchema):
    id: UUID
    repo_id: UUID
    user_id: UUID
    analyzed_at: datetime

    class Config:
        from_attributes = True

# Recruiter Simulation Schemas
class RecruiterSimulationSchema(BaseModel):
    target_role: str
    company_tier: str
    verdict: str
    confidence: str
    reasoning: str
    biggest_fix: str
    would_reach_out: bool

# Project Recommendation Schemas
class ProjectRecommendationSchema(BaseModel):
    title: str
    description: str
    tech_stack: List[str]
    complexity_tier: str
    score_boost_est: float
    gaps_filled: List[str]
    build_hours_est: int

# Profile Summary
class ProfileSummary(BaseModel):
    username: str
    overall_score: float
    grade: str
    repos_analyzed: int
    top_repos: List[Repository]
    recent_analyses: List[AnalysisSchema]
    recruiter_verdict: Optional[str] = None
