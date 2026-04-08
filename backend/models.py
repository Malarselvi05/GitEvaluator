from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, ARRAY, JSON, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(255))
    access_token = Column(Text)  # Encrypted in production
    plan = Column(String(20), default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_analyzed = Column(DateTime(timezone=True))

    repositories = relationship("Repository", back_populates="user", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    snapshots = relationship("ProfileSnapshot", back_populates="user", cascade="all, delete-orphan")
    simulations = relationship("RecruiterSimulation", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("ProjectRecommendation", back_populates="user", cascade="all, delete-orphan")

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", on_delete="CASCADE"))
    github_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    description = Column(Text)
    language = Column(String(100))
    topics = Column(ARRAY(String))
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    is_fork = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    pushed_at = Column(DateTime(timezone=True))
    raw_data = Column(JSONB)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="repositories")
    analysis = relationship("Analysis", back_populates="repository", uselist=False, cascade="all, delete-orphan")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id", on_delete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", on_delete="CASCADE"))
    code_quality_score = Column(Integer)
    impact_score = Column(Integer)
    innovation_score = Column(Integer)
    completeness_score = Column(Integer)
    relevance_score = Column(Integer)
    composite_score = Column(Numeric(5, 2))
    complexity_tier = Column(String(20))
    is_commodity_project = Column(Boolean, default=False)
    resume_worthy = Column(Boolean)
    one_line_summary = Column(Text)
    ai_reasoning = Column(JSONB)
    improvement_actions = Column(JSONB)
    resume_bullet = Column(Text)
    generated_readme = Column(Text)
    linkedin_description = Column(Text)
    model_used = Column(String(100))
    tokens_used = Column(Integer)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())

    repository = relationship("Repository", back_populates="analysis")
    user = relationship("User", back_populates="analyses")

class ProfileSnapshot(Base):
    __tablename__ = "profile_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", on_delete="CASCADE"))
    overall_score = Column(Numeric(5, 2))
    grade = Column(String(5))
    repos_analyzed = Column(Integer)
    recruiter_verdict = Column(String(20))
    snapshot_data = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="snapshots")

class RecruiterSimulation(Base):
    __tablename__ = "recruiter_simulations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", on_delete="CASCADE"))
    target_role = Column(String(100))
    company_tier = Column(String(50))
    verdict = Column(String(20))
    confidence = Column(String(10))
    reasoning = Column(Text)
    biggest_fix = Column(Text)
    would_reach_out = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="simulations")

class ProjectRecommendation(Base):
    __tablename__ = "project_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", on_delete="CASCADE"))
    title = Column(String(255))
    description = Column(Text)
    tech_stack = Column(ARRAY(String))
    complexity_tier = Column(String(20))
    score_boost_est = Column(Numeric(4, 1))
    gaps_filled = Column(ARRAY(String))
    build_hours_est = Column(Integer)
    is_dismissed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="recommendations")
