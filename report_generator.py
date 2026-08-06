import json
from config import model


# ==========================================
# Generate AI Career Report
# ==========================================

def generate_report(skill, location, industry_data, jobs):
    """
    Generates a concise AI career report using Gemini.
    """

    # Send only useful job fields to Gemini
    simplified_jobs = []

    for job in jobs:
        simplified_jobs.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location")
        })

    prompt = f"""
You are SkillMap AI.

Generate a SHORT professional report.

Skill:
{skill}

Location:
{location}

Industry Research:
{industry_data}

Rules:

Maximum 120 words.

Return ONLY markdown.

Format:

# 📊 AI Career Report

⭐ Demand:
(Very High / High / Medium / Low)

🏭 Top Industries
• ...
• ...
• ...

💼 Top Roles
• ...
• ...
• ...

📈 Career Outlook
(2 short sentences)

🚀 Learning Focus
• ...
• ...
• ...
• ...
"""

    response = model.invoke(prompt)

    return response.content


# ==========================================
# Format Top 10 Jobs
# ==========================================

def format_jobs(jobs):

    if not jobs:
        return "# 💼 Live Jobs\n\nNo jobs found."

    output = "# 💼 Live Jobs\n\n"

    for i, job in enumerate(jobs, start=1):

        output += f"""
### {i}. {job['title']}

🏢 **Company:** {job['company']}

📍 **Location:** {job['location']}

💼 **Type:** {job['employment_type']}

💰 **Salary:** {job['salary']}

🔗 **Apply:** {job['apply_link']}

---
"""

    return output