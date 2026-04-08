import os
from celery import Celery
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas
from sqlalchemy.sql import func
from .services.github_service import GitHubService
from .services.ai_service import AIService
from .services.heuristic_service import HeuristicService
from dotenv import load_dotenv

load_dotenv()

# Celery instance
celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

@celery_app.task(name="analyze_profile_task")
def analyze_profile_task(user_id: str, github_username: str, access_token: str):
    db = SessionLocal()
    try:
        gh_service = GitHubService(access_token)
        ai_service = AIService()
        heuristic_service = HeuristicService()

        # 1. Fetch all repos
        repos_data = gh_service.get_user_repos()
        
        # 2. Store or update repos in DB
        for repo_info in repos_data:
            repo = db.query(models.Repository).filter(
                models.Repository.github_id == repo_info['id']
            ).first()
            
            if not repo:
                repo = models.Repository(
                    user_id=user_id,
                    github_id=repo_info['id'],
                    name=repo_info['name'],
                    full_name=repo_info['full_name'],
                    description=repo_info.get('description'),
                    language=repo_info.get('language'),
                    topics=repo_info.get('topics', []),
                    stars=repo_info.get('stargazers_count', 0),
                    forks=repo_info.get('forks_count', 0),
                    is_fork=repo_info.get('fork', False),
                    raw_data=repo_info
                )
                db.add(repo)
        
        db.commit()

        # 3. Analyze top repos
        user_repos = db.query(models.Repository).filter(
            models.Repository.user_id == user_id
        ).order_by(models.Repository.stars.desc()).limit(5).all()

        for repo in user_repos:
            # Fetch deep data for AI analysis
            readme = gh_service.get_repo_readme(repo.full_name.split('/')[0], repo.name)
            tree = gh_service.get_repo_tree(repo.full_name.split('/')[0], repo.name)
            commits = gh_service.get_repo_commits(repo.full_name.split('/')[0], repo.name)

            # Heuristic Analysis
            completeness = heuristic_service.calculate_completeness_score(readme or "", tree)

            analysis_input = {
                "name": repo.name,
                "language": repo.language,
                "description": repo.description,
                "topics": repo.topics,
                "readme": readme,
                "tree": tree,
                "commits": commits,
                "stars": repo.stars,
                "forks": repo.forks
            }

            # AI Analysis
            ai_result = ai_service.analyze_repo(analysis_input)

            if "error" not in ai_result:
                # Save analysis
                analysis = models.Analysis(
                    repo_id=repo.id,
                    user_id=user_id,
                    code_quality_score=ai_result.get('code_quality', {}).get('score', 0),
                    impact_score=ai_result.get('impact', {}).get('score', 0),
                    innovation_score=ai_result.get('innovation', {}).get('score', 0),
                    completeness_score=completeness['score'],
                    relevance_score=ai_result.get('industry_relevance', {}).get('score', 0),
                    complexity_tier=ai_result.get('complexity_tier', 'beginner'),
                    is_commodity_project=ai_result.get('innovation', {}).get('is_commodity_project', False),
                    resume_worthy=ai_result.get('resume_worthy', False),
                    one_line_summary=ai_result.get('one_line_summary', ''),
                    ai_reasoning={
                        "ai": ai_result,
                        "heuristics": completeness['details']
                    },
                    improvement_actions=ai_result.get('improvement_actions', [])
                )
                
                # Composite score (Average of all 5 dimensions)
                analysis.composite_score = (
                    analysis.code_quality_score + 
                    analysis.impact_score + 
                    analysis.innovation_score + 
                    analysis.completeness_score +
                    analysis.relevance_score
                ) / 1.0 # Result is out of 100 correctly because each is 0-20
                
                db.add(analysis)
        
        db.commit()
        
        # 4. Update user's last_analyzed
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.last_analyzed = func.now()
            db.commit()

    except Exception as e:
        print(f"Error in analysis task: {e}")
    finally:
        db.close()
