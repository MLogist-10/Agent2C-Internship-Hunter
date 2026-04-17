import os
import json
import time
from google import genai
from dotenv import load_dotenv
from app.agent.profile import PROFILE
from app.database.operations import get_unscored_jobs, update_ai_score

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version':'v1beta'})


def build_prompt(job):
    return f"""

You are an AI career assistant helping a student find the best internship matches.


Student Profile:

- Name: {PROFILE['name']}
- Skills: {', '.join(PROFILE['skills'])}
- Interests: {', '.join(PROFILE['interests'])}
- Location preference: {', '.join(PROFILE['location_preference'])}
- Minimum stipend: ₹{PROFILE['stipend_minimum']}/month
- Level: {PROFILE['experience_level']}
- About: {PROFILE['about']}

Job Listing:
- Title: {job['title']}
- Company: {job['company']}
- Location: {job['location']}
- Stipend: {job['stipend']}
- Duration: {job['duration']}
- URL: {job['url']}

Task:
Score this job for how well it matches the student profile.
Score from 1 to 10 where:
- 1-3 = Poor fit
- 4-6 = Decent fit
- 7-8 = Good fit
- 9-10 = Excellent fit

Respond ONLY in this exact JSON format, nothing else:
{{
    "score": <integer 1-10>,
    "reason": "<one sentence explaining the score>"
}}
"""

def score_job(job):
    prompt = build_prompt(job)
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        text = response.text.strip()

        text = text.replace("```json", "").replace("```","").strip()

        result = json.loads(text)
        score = int(result["score"])
        reason = result["reason"]
        return score, reason
    

    except Exception as e:
        print(f"  Scoring error for {job['title']}: {e}")
        return 0, "Could not score"
    
def run_agent():
    jobs = get_unscored_jobs()
    print(f"\nAgent starting - {len(jobs)} unscored jobs found\n")

    if not jobs:
        print("All jobs already scored.")
        return

    for i, job in enumerate(jobs):
        print(f"Scoring: {job['title']} at {job['company']}")
        score, reason = score_job(job)
        update_ai_score(job["id"], score, reason)

        print(f"  Score: {score}/10 - {reason}")
        time.sleep(4)
    print(f"\nAgent done. {len(jobs)} jobs scored.")