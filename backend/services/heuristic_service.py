import re
from typing import List, Dict, Any

class HeuristicService:
    @staticmethod
    def calculate_completeness_score(readme_content: str, file_tree: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 0
        details = []

        # 1. README present (assumed since we have content, but let's check tree)
        has_readme = any(f['path'].lower() == 'readme.md' or f['path'].lower() == 'readme' for f in file_tree)
        if has_readme:
            score += 4
            details.append("README present (+4)")

        if readme_content:
            # 2. Setup / Installation section
            if re.search(r'#+\s*(installation|setup|getting started)', readme_content, re.IGNORECASE):
                score += 3
                details.append("Setup section found (+3)")
            
            # 3. Requirements / Dependencies
            if re.search(r'#+\s*(requirements|dependencies|prerequisites)', readme_content, re.IGNORECASE) or \
               any(f['path'] in ['requirements.txt', 'package.json', 'go.mod', 'Gemfile', 'Cargo.toml'] for f in file_tree):
                score += 3
                details.append("Dependencies documented (+3)")
            
            # 4. Demo link or screenshot
            if re.search(r'!\[.*\]\(.*\)|http', readme_content):
                score += 1
                details.append("Demo/Media link found (+1)")

        # 5. Tests directory
        has_tests = any(re.search(r'test', f['path'], re.IGNORECASE) for f in file_tree if f['type'] == 'tree')
        if has_tests:
            score += 4
            details.append("Tests directory found (+4)")

        # 6. CI/CD config
        has_cicd = any(f['path'].startswith('.github/workflows') or f['path'] in ['.travis.yml', 'circle.yml'] for f in file_tree)
        if has_cicd:
            score += 3
            details.append("CI/CD configuration found (+3)")

        # 7. License
        has_license = any(re.search(r'license', f['path'], re.IGNORECASE) for f in file_tree)
        if has_license:
            score += 2
            details.append("License file found (+2)")

        return {
            "score": min(score, 20),
            "details": details
        }

    @staticmethod
    def calculate_tech_stack_score(languages: Dict[str, int]) -> int:
        # Simplified demand index from the plan
        # Python + ML: 20, TS+React: 18, etc.
        primary = max(languages, key=languages.get) if languages else ""
        
        scores = {
            "Python": 20, # Assuming ML focus in this context
            "TypeScript": 18,
            "JavaScript": 16,
            "Rust": 17,
            "Go": 17,
            "Java": 14,
            "C++": 18,
            "Ruby": 12,
            "PHP": 8
        }
        
        return scores.get(primary, 10)
