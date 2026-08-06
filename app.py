import os
import traceback
import gradio as gr
import time

from industry import get_industry_demand
from job_search import search_jobs
from report_generator import generate_report, format_jobs


# =====================================================
# Career Agent
# =====================================================

def career_agent(skill, location):

    # Handle empty input safely
    skill = (skill or "").strip()
    location = (location or "").strip()

    if not skill:
        return (
            "⚠️ Please enter a skill or job role.",
            "",
            "N/A",
            "0 Jobs"
        )

    if not location:
        return (
            "⚠️ Please enter a location.",
            "",
            "N/A",
            "0 Jobs"
        )

    print("\n" + "=" * 60)
    print(f"Skill    : {skill}")
    print(f"Location : {location}")

    total_start = time.time()

    # -------------------------------------------------
    # Industry Research
    # -------------------------------------------------

    try:

        start = time.time()

        industry = get_industry_demand(skill)

        print(f"✅ Industry Time : {time.time()-start:.2f} sec")

    except Exception as e:

        print("❌ Industry Error :", e)

        industry = "Industry information unavailable."

    # -------------------------------------------------
    # Job Search
    # -------------------------------------------------

    try:

        start = time.time()

        jobs = search_jobs(skill, location)

        print(f"✅ Jobs Time : {time.time()-start:.2f} sec")
        print(f"Jobs Found : {len(jobs)}")

    except Exception as e:

        print("❌ Job Search Error :", e)

        jobs = []

    # -------------------------------------------------
    # AI Report
    # -------------------------------------------------

    try:

        start = time.time()

        report = generate_report(
            skill,
            location,
            industry,
            jobs
        )

        print(f"✅ Gemini Time : {time.time()-start:.2f} sec")

    except Exception as e:

        print("❌ Gemini Error :", e)

        report = f"""
# 📊 AI Career Report

AI report could not be generated.

Reason:

{e}

Live jobs are still displayed below.
"""

    print(f"🚀 Total Time : {time.time()-total_start:.2f} sec")
    print("=" * 60)

    # -------------------------------------------------
    # Format Jobs
    # -------------------------------------------------

    jobs_output = format_jobs(jobs)

    # -------------------------------------------------
    # Skill Demand
    # -------------------------------------------------

    report_lower = report.lower()

    if "very high" in report_lower:
        demand = "⭐⭐⭐⭐⭐ Very High"

    elif "high" in report_lower:
        demand = "⭐⭐⭐⭐ High"

    elif "medium" in report_lower:
        demand = "⭐⭐⭐ Medium"

    elif "low" in report_lower:
        demand = "⭐⭐ Low"

    else:
        demand = "Unknown"

    return (
        report,
        jobs_output,
        demand,
        f"{len(jobs)} Jobs"
    )

# =====================================================
# Theme
# =====================================================

theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="sky",
    neutral_hue="gray",
).set(
    body_background_fill="#F8FAFC",
    block_background_fill="#FFFFFF",
    block_border_color="#E2E8F0",
    block_radius="12px",
    button_primary_background_fill="#2563EB",
    button_primary_background_fill_hover="#1D4ED8"
)


# =====================================================
# JavaScript
# =====================================================

scroll_js = """
() => {

    setTimeout(() => {

        const report =
        document.getElementById("career-report");

        if(report){

            report.scrollIntoView({
                behavior:"smooth",
                block:"start"
            });

        }

    },300);

}
"""

with gr.Blocks(
    title="SkillMap AI"
) as demo:

    # =====================================================
    # Hero Banner
    # =====================================================

    gr.HTML("""

    <div class="hero">

        <h1>🚀 SkillMap AI</h1>

        <h2>
            AI-Powered Career Navigator
        </h2>

        <p>

        Discover career opportunities with

        <b>Industry Demand</b>,
        <b>AI Career Reports</b> &
        <b>Live Job Listings</b>.

        </p>

    </div>

    """)

    # =====================================================
    # Search Section
    # =====================================================

    with gr.Group():

        with gr.Row():

            skill = gr.Textbox(

                label="🎯 Skill / Job Role",

                placeholder="Enter a skill or job role",

                scale=2

            )

            location = gr.Textbox(

                label="📍 Preferred Location",

                placeholder="Enter city or country",

                scale=2

            )

        search_btn = gr.Button(

            "🚀 Analyze Career",

            variant="primary",

            size="lg"

        )

    gr.Markdown("---")

    # =====================================================
    # Dashboard Cards
    # =====================================================

    with gr.Row():

        demand_card = gr.Textbox(

            label="📈 Skill Demand",

            interactive=False,

            scale=1

        )

        jobs_card = gr.Textbox(

            label="💼 Jobs Found",

            interactive=False,

            scale=1

        )

    gr.Markdown("---")

    # =====================================================
    # Results Anchor
    # =====================================================

    gr.HTML(

        """
        <div id="career-report"></div>
        """

    )

    # =====================================================
    # AI Report
    # =====================================================

    report_output = gr.Markdown(

        value="""

# 📊 AI Career Report

Click **🚀 Analyze Career**

to generate your personalized report.

""",

        height=350

    )

    gr.Markdown("---")

    # =====================================================
    # Live Jobs
    # =====================================================

    jobs_output = gr.Markdown(

        value="""

# 💼 Live Jobs

Your live jobs will appear here.

""",

        height=650

    )

    gr.Markdown("---") 


    # =====================================================
    # Search Action
    # =====================================================

    search_btn.click(
        fn=career_agent,
        inputs=[skill, location],
        outputs=[
            report_output,
            jobs_output,
            demand_card,
            jobs_card,
        ],
        show_progress="full"
    )


    # =====================================================
    # Footer
    # =====================================================

    gr.HTML("""

    <div class="footer">

    <hr>

    <h2>🚀 SkillMap AI</h2>

    <p>

    AI-Powered Career Navigator

    </p>

    <p>

    Built with

    <b>Google Gemini 2.5 Flash</b> •
    <b>Tavily Search</b> •
    <b>Active Jobs DB API</b> •
    <b>Gradio</b>

    </p>

    <p>

    Version 1.0

    </p>

    <p>

    Developed by
    <b>Buvashid Chavan</b>

    </p>

    </div>

    """)

# =====================================================
# Launch
# =====================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    demo.launch(
    server_name="0.0.0.0",
    server_port=port,
    theme=theme,
    css=open("styles.css").read(),
    show_error=True
)
