import requests
from config import RAPID_API_KEY


def search_jobs(skill, location, limit=10):
    """
    Search jobs using Active Jobs DB API.
    """

    url = "https://active-jobs-db.p.rapidapi.com/active-ats"

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "active-jobs-db.p.rapidapi.com"
    }

    params = {
        "title": skill,
        "location": location,
        "time_frame": "24h",
        "limit": str(limit),
        "offset": "0",
        "description_format": "text"
    }

    # -------------------------------------------------------
    # First Search (Skill + Location)
    # -------------------------------------------------------

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        print("=" * 70)
        print("Status Code :", response.status_code)
        print("Request URL :", response.url)

        if response.status_code != 200:
            print(response.text)
            return []

        data = response.json()

    except Exception as e:

        print("API Error :", e)
        return []


    # -------------------------------------------------------
    # Retry without location if nothing found
    # -------------------------------------------------------

    if len(data) == 0:

        print("No jobs found. Retrying without location...")

        params["location"] = ""

        try:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()

        except Exception:
            pass

        

    jobs = []

    # -------------------------------------------------------
    # Parse Jobs
    # -------------------------------------------------------

    for job in data[:limit]:

        # Location
        location_text = "Not Specified"

        locations = job.get("locations")

        if isinstance(locations, list) and len(locations) > 0:

            address = locations[0].get("address", {})

            location_text = (
                address.get("streetAddress")
                or address.get("addressLocality")
                or "Not Specified"
            )

        # Employment Type
        employment = (
            job.get("employment_type")
            or job.get("ai_employment_type")
        )

        if isinstance(employment, list):
            employment = ", ".join(employment)

        if not employment:
            employment = "Not Specified"

        # Salary
        salary = "Not Mentioned"

        if job.get("salary"):

            value = job["salary"].get("value", {})

            minimum = value.get("minValue")
            maximum = value.get("maxValue")

            if minimum or maximum:
                salary = f"{minimum or ''} - {maximum or ''}"

        # Remote
        location_type = job.get("location_type") or ""

        remote = location_type.upper() == "TELECOMMUTE"

        jobs.append({

            "title": job.get("title", "N/A"),

            "company": job.get("organization", "N/A"),

            "location": location_text,

            "employment_type": employment,

            "remote": remote,

            "salary": salary,

            "posted": job.get("date_posted", ""),

            "description": job.get("description_text", ""),

            "apply_link": job.get("url", "#"),

            "company_logo": job.get("organization_logo")

        })

    print("=" * 70)
    print(f"Found {len(jobs)} jobs")
    print("=" * 70)

    return jobs