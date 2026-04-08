import os
import json
from anthropic import Anthropic
from openai import OpenAI
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def analyze_repo(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes a repository using Claude.
        repo_data should contain: name, language, description, topics, readme, tree, commits
        """
        
        system_prompt = """
        You are a senior software engineering hiring manager and code reviewer with 10+ years of experience 
        evaluating developer portfolios at top tech companies. You evaluate GitHub repositories objectively 
        and provide scores as structured JSON.
        """
        
        user_prompt = f"""
        Analyze this GitHub repository and return scores matching the schema.

        Repository: {repo_data.get('name')}
        Primary Language: {repo_data.get('language')}
        Description: {repo_data.get('description')}
        Topics: {repo_data.get('topics')}
        Stars: {repo_data.get('stars')} | Forks: {repo_data.get('forks')}

        README Content Summary (First 2000 chars):
        {repo_data.get('readme', '')[:2000]}

        File Structure (Selection):
        {json.dumps([f['path'] for f in repo_data.get('tree', [])[:40]], indent=2)}

        Recent Commit Messages:
        {json.dumps([c.get('commit', {}).get('message', '') for c in repo_data.get('commits', [])[:10]], indent=2)}

        Return ONLY valid JSON matching this schema:
        {{
          "code_quality": {{
            "score": <0-20>,
            "top_issue": "<15 words max>",
            "improvement": "<20 words max>"
          }},
          "impact": {{
            "score": <0-20>,
            "top_issue": "<15 words max>",
            "improvement": "<20 words max>"
          }},
          "innovation": {{
            "score": <0-20>,
            "is_commodity_project": <true|false>,
            "top_issue": "<15 words max>",
            "improvement": "<20 words max>"
          }},
          "industry_relevance": {{
            "score": <0-20>,
            "detected_stack": ["<tech1>", "<tech2>"],
            "top_issue": "<15 words max>",
            "improvement": "<20 words max>"
          }},
          "complexity_tier": "<beginner|intermediate|advanced>",
          "resume_worthy": <true|false>,
          "one_line_summary": "<20 words max>"
        }}
        """

        message = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        try:
            # Extract JSON from the response
            content = message.content[0].text
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return {
                "error": "Failed to parse AI response",
                "raw_content": message.content[0].text
            }

    async def classify_complexity(self, repo_summary: str) -> str:
        """
        Quickly classifies repo complexity using Claude Haiku.
        """
        system_prompt = "You are a senior dev. Classify repo complexity as beginner, intermediate, or advanced."
        user_prompt = f"Analyze this repo summary and return ONLY the tier: {repo_summary}"

        message = self.anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            temperature=0,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return message.content[0].text.strip().lower()

    async def simulate_recruiter(self, profile_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates a recruiter's response to the profile using Claude Sonnet.
        """
        system_prompt = """
        You are a Senior Technical Recruiter at a top-tier tech company. 
        You see hundreds of GitHub profiles daily. Provide a blunt, honest assessment.
        """
        
        user_prompt = f"""
        Profile Summary: {json.dumps(profile_summary, indent=2)}
        
        Return JSON matching this schema:
        {{
          "verdict": "Strong Hire | Shortlist | Reject",
          "confidence": "High | Medium | Low",
          "reasoning": "2 sentences max",
          "biggest_fix": "Single most impactful action",
          "would_reach_out": true|false
        }}
        """

        message = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        try:
            return json.loads(message.content[0].text)
        except:
            return {"error": "Failed to parse simulation"}
