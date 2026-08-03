"""Job search service — find FinTech jobs matching Jevgeni's skills."""
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

CURATED_FINTECH_JOBS = [
    {
        "title": "Senior Full-Stack Engineer (FinTech)",
        "company": "Trade Republic",
        "location": "Berlin / Remote Germany",
        "url": "https://traderepublic.com/careers",
        "skills": ["Python", "React", "TypeScript", "FastAPI", "Kubernetes"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Quantitative Developer",
        "company": "N26",
        "location": "Berlin / Remote",
        "url": "https://n26.com/en/careers",
        "skills": ["Python", "C++", "Rust", "Financial Math", "Algorithms"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Senior Software Engineer — Trading Platform",
        "company": "Lunar Bank",
        "location": "Frankfurt / Remote EU",
        "url": "https://lunar.app/en/careers",
        "skills": ["Python", "Go", "React", "PostgreSQL", "Redis"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Lead Backend Engineer — Financial Data Platform",
        "company": "Mambu",
        "location": "Berlin / Remote",
        "url": "https://www.mambu.com/en/careers",
        "skills": ["Java", "Python", "AWS", "Microservices", "SQL"],
        "match": "medium",
        "source": "curated",
    },
    {
        "title": "Senior Quant Engineer — Options Market Making",
        "company": "Flow Traders",
        "location": "Amsterdam / Remote",
        "url": "https://www.flowtraders.com/careers",
        "skills": ["Python", "C++", "Quant Finance", "Probability", "Statistics"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Software Engineer — Risk Analytics",
        "company": "Deutsche Börse",
        "location": "Frankfurt / Remote",
        "url": "https://deutsche-boerse.com/careers",
        "skills": ["Python", "Java", "SQL", "Risk Models", "Data Analysis"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Full-Stack Developer — Wealth Management Platform",
        "company": "Scalable Capital",
        "location": "Munich / Remote",
        "url": "https://de.scalable.capital/careers",
        "skills": ["TypeScript", "React", "Python", "AWS", "Docker"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Senior Python Developer — Payments Infrastructure",
        "company": "Klarna",
        "location": "Berlin / Remote",
        "url": "https://www.klarna.com/careers",
        "skills": ["Python", "PostgreSQL", "Kafka", "AWS", "Microservices"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Blockchain Engineer — DeFi Platform",
        "company": "1inch",
        "location": "Remote EU",
        "url": "https://1inch.io/careers",
        "skills": ["Solidity", "Python", "Web3", "Ethereum", "TypeScript"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Principal Engineer — AI for Finance",
        "company": "BlackRock (Frankfurt office)",
        "location": "Frankfurt / Remote",
        "url": "https://careers.blackrock.com",
        "skills": ["Python", "ML", "LLMs", "Financial Data", "Cloud"],
        "match": "medium",
        "source": "curated",
    },
    {
        "title": "Senior DevOps Engineer — FinTech Infrastructure",
        "company": "Wealthsimple",
        "location": "Remote EU",
        "url": "https://www.wealthsimple.com/en-ca/careers",
        "skills": ["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD"],
        "match": "high",
        "source": "curated",
    },
    {
        "title": "Lead Product Engineer — Trading Terminal",
        "company": "Capitolis",
        "location": "Remote / Frankfurt",
        "url": "https://www.capitolis.com/careers",
        "skills": ["React", "Node.js", "Python", "Financial Services", "Real-time Data"],
        "match": "high",
        "source": "curated",
    },
]

SKILL_TAGS = {
    "high": ["Python", "React", "TypeScript", "FastAPI", "Docker", "Kubernetes", "PostgreSQL",
             "Redis", "AI", "ML", "Quant", "Finance", "Trading", "Crypto", "Web3",
             "Stripe", "APIs", "REST", "Full-Stack", "Cloud", "AWS", "GCP"],
    "medium": ["Java", "C#", "Go", "C++", "Rust", "ERP", "SAP", "IT Operations"],
}


async def search_jobs(skill: str = "", location: str = "Germany", remote: bool = True) -> list[dict]:
    """Search curated FinTech jobs matching Jevgeni's profile."""
    results = []
    query = skill.lower() if skill else ""

    for job in CURATED_FINTECH_JOBS:
        score = 0
        # Location match
        if location.lower() in job["location"].lower():
            score += 2
        if remote and "remote" in job["location"].lower():
            score += 2

        # Skill match
        if query:
            job_skills = " ".join(job["skills"]).lower()
            job_all = f"{job['title']} {job['company']} {job_skills}"
            if query in job_all:
                score += 3

        # Match level
        if job["match"] == "high":
            score += 3
        elif job["match"] == "medium":
            score += 1

        results.append({**job, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return [r for r in results if r["score"] > 0] if query or location != "Germany" else results[:15]


async def search_github_jobs(query: str = "fintech") -> list[dict]:
    """Search GitHub Jobs API for matching positions."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                "https://jobs.github.com/positions.json",
                params={"description": query, "location": "germany"},
                headers={"User-Agent": "Miau-Finance/1.0"},
            )
            if r.status_code == 200:
                jobs = r.json()
                return [
                    {
                        "title": j.get("title", "?"),
                        "company": j.get("company", "?"),
                        "location": j.get("location", "?"),
                        "url": j.get("url", "?"),
                        "skills": [query],
                        "match": "unknown",
                        "source": "github_jobs",
                    }
                    for j in jobs[:20]
                ]
    except Exception as e:
        logger.warning("GitHub Jobs search failed: %s", e)
    return []


async def get_job_summary() -> dict:
    """Get a summary of available job matches."""
    all_jobs = await search_jobs()
    high_match = [j for j in all_jobs if j["match"] == "high"]
    companies = list(set(j["company"] for j in high_match))
    skills_needed = list(set(
        s for j in high_match for s in j["skills"]
    ))
    return {
        "total_matches": len(all_jobs),
        "high_match_count": len(high_match),
        "companies": sorted(companies),
        "top_skills_demanded": sorted(skills_needed)[:15],
        "cat_commentary": "The cat reviewed the job market. The cat says you're overqualified. Apply anyway. 🐱",
    }
