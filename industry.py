from config import tavily

def get_industry_demand(skill: str):

    query = f"""
    Give the latest market analysis for {skill}.

    Include:
    - Demand Level
    - Top Hiring Industries
    - Career Outlook
    - Salary Trends
    - Future Growth

    Return concise information.
    """

    result = tavily.invoke(query)

    return result