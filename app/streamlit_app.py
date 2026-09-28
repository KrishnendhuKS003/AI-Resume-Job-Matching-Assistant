import html
import tempfile
from pathlib import Path

import streamlit as st

from genai.full_pipeline import analyze_resume_file


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResumeMatch AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# LOAD CSS
# ============================================================

STYLE_PATH = Path("app/style.css")

if not STYLE_PATH.exists():
    st.error("app/style.css could not be found.")
    st.stop()

st.html(STYLE_PATH)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "current_page": "home",
    "analysis_result": None,
    "resume_data": None,
    "job_description_data": "",
    "scroll_to_top": False,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# NAVIGATION
# ============================================================

def navigate_to(page):
    st.session_state.current_page = page
    st.session_state.scroll_to_top = True
    st.rerun()


# ============================================================
# RESET FOR A COMPLETELY NEW ANALYSIS
# ============================================================

def start_new_analysis():

    st.session_state.analysis_result = None
    st.session_state.resume_data = None
    st.session_state.job_description_data = ""

    for key in [
        "resume_upload",
        "job_description",
        "analyze_resume_button",
    ]:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.current_page = "analysis"
    st.session_state.scroll_to_top = True

    st.rerun()


# ============================================================
# SCROLL TO TOP
# ============================================================

if st.session_state.scroll_to_top:

    st.session_state.scroll_to_top = False

    st.html(
        """
        <script>
        setTimeout(function () {

            const containers = [
                document.querySelector('[data-testid="stAppViewContainer"]'),
                document.querySelector('[data-testid="stMain"]'),
                document.querySelector('section.main'),
                document.querySelector('.main')
            ];

            containers.forEach(function(container) {
                if (container) {
                    container.scrollTo({
                        top: 0,
                        left: 0,
                        behavior: 'instant'
                    });
                }
            });

            window.scrollTo({
                top: 0,
                left: 0,
                behavior: 'instant'
            });

        }, 100);
        </script>
        """,
        unsafe_allow_javascript=True,
    )


# ============================================================
# NAVIGATION BAR
# ============================================================

brand_column, home_column, analysis_column, results_column = st.columns(
    [4, 1, 1, 1],
    vertical_alignment="center",
)


# ------------------------------------------------------------
# BRAND
# ------------------------------------------------------------

with brand_column:

    st.html(
        """
        <div class="brand">
            🤖 ResumeMatch AI
        </div>
        """
    )


# ------------------------------------------------------------
# HOME NAVIGATION
# ------------------------------------------------------------

with home_column:

    if st.session_state.current_page == "home":

        clicked = st.button(
            "Home",
            key="nav_home",
            type="primary",
            use_container_width=True,
        )

    else:

        clicked = st.button(
            "Home",
            key="nav_home",
            type="secondary",
            use_container_width=True,
        )

    if clicked:
        navigate_to("home")


# ------------------------------------------------------------
# ANALYSIS NAVIGATION
# ------------------------------------------------------------

with analysis_column:

    if st.session_state.current_page == "analysis":

        clicked = st.button(
            "Analysis",
            key="nav_analysis",
            type="primary",
            use_container_width=True,
        )

    else:

        clicked = st.button(
            "Analysis",
            key="nav_analysis",
            type="secondary",
            use_container_width=True,
        )

    if clicked:
        navigate_to("analysis")


# ------------------------------------------------------------
# RESULTS NAVIGATION
# ------------------------------------------------------------

with results_column:

    if st.session_state.current_page == "results":

        clicked = st.button(
            "Results",
            key="nav_results",
            type="primary",
            use_container_width=True,
        )

    else:

        clicked = st.button(
            "Results",
            key="nav_results",
            type="secondary",
            use_container_width=True,
        )

    if clicked:

        if st.session_state.analysis_result is not None:
            navigate_to("results")
        else:
            st.toast(
                "Analyze a resume first to view results."
            )


st.html(
    """
    <div class="nav-divider"></div>
    """
)


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.current_page == "home":

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.html(
        """
        <div class="hero">

            <div class="hero-badge">
                ✦ AI-Powered Resume Analysis
            </div>

            <div class="hero-title">
                Find out how well your resume
                matches the job.
            </div>

            <div class="hero-description">
                ResumeMatch AI analyzes your resume against a job
                description to identify your strengths, missing skills,
                experience alignment, and areas you can improve.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # FEATURE INTRODUCTION
    # --------------------------------------------------------

    st.html(
        """
        <div class="page-header">

            <div class="page-title">
                Everything you need to understand your match
            </div>

            <div class="page-description">
                Go beyond a simple keyword comparison and get a clearer
                picture of how your resume fits a specific opportunity.
            </div>

        </div>
        """
    )


    feature_1, feature_2, feature_3 = st.columns(
        3,
        gap="large",
    )


    with feature_1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon icon-lavender">
                    🎯
                </div>

                <div class="feature-title">
                    Overall Match
                </div>

                <div class="feature-text">
                    Get a clear match score that combines different
                    aspects of resume and job-description similarity.
                </div>

            </div>
            """
        )


    with feature_2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon icon-sage">
                    🧩
                </div>

                <div class="feature-title">
                    Skill Analysis
                </div>

                <div class="feature-text">
                    See which skills match the job requirements and
                    which important skills may be missing.
                </div>

            </div>
            """
        )


    with feature_3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon icon-peach">
                    💡
                </div>

                <div class="feature-title">
                    AI Suggestions
                </div>

                <div class="feature-text">
                    Receive useful recommendations to help improve
                    the alignment between your resume and the role.
                </div>

            </div>
            """
        )


    # --------------------------------------------------------
    # HOW IT WORKS
    # --------------------------------------------------------

    st.html(
        """
        <div class="page-header">

            <div class="page-title">
                How ResumeMatch AI works
            </div>

            <div class="page-description">
                A simple process designed to make resume analysis
                easy to understand.
            </div>

        </div>
        """
    )


    step_1, step_2, step_3, step_4 = st.columns(
        4,
        gap="medium",
    )


    steps = [
        (
            step_1,
            "01",
            "Upload Resume",
            "Add your resume as a PDF or DOCX file.",
        ),
        (
            step_2,
            "02",
            "Add Job Description",
            "Enter or paste the job description you want to target.",
        ),
        (
            step_3,
            "03",
            "Analyze",
            "ResumeMatch AI compares your resume with the job requirements.",
        ),
        (
            step_4,
            "04",
            "Understand Results",
            "Explore your match, skills, experience, education, and recommendations.",
        ),
    ]


    for column, number, title, description in steps:

        with column:

            st.html(
                f"""
                <div class="section-card">

                    <div class="page-label">
                        {number}
                    </div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-text">
                        {description}
                    </div>

                </div>
                """
            )


    # --------------------------------------------------------
    # WHY USE IT
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-card">

            <div class="page-label">
                WHY RESUMEMATCH AI?
            </div>

            <div class="page-title">
                Make your resume more targeted
                for every opportunity.
            </div>

            <div class="page-description">
                Instead of using the same resume for every application,
                analyze it against the specific role you are applying for.
                ResumeMatch AI helps you understand where your resume
                already aligns and where it could be strengthened.
            </div>

            <br>

            <div class="info-content">
                ✓ Compare your resume with a specific job description
            </div>

            <div class="info-content">
                ✓ Identify matching and missing skills
            </div>

            <div class="info-content">
                ✓ Understand experience and education alignment
            </div>

            <div class="info-content">
                ✓ Get actionable resume improvement suggestions
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # GET STARTED
    # --------------------------------------------------------

    st.html(
        """
        <div class="hero">

            <div class="hero-badge">
                🚀 Get Started
            </div>

            <div class="page-title">
                Ready to check your resume?
            </div>

            <div class="page-description">
                Upload your resume and add the job description
                to start your personalized analysis.
            </div>

        </div>
        """
    )


    start_left, start_middle, start_right = st.columns(
        [2, 2, 2],
    )


    with start_middle:

        if st.button(
            "Get Started  →",
            key="get_started_button",
            type="secondary",
            use_container_width=True,
        ):
            navigate_to("analysis")


# ============================================================
# ANALYSIS PAGE
# ============================================================

elif st.session_state.current_page == "analysis":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="page-header">

            <div class="page-label">
                Resume Analysis
            </div>

            <div class="page-title">
                Analyze your resume
            </div>

            <div class="page-description">
                Upload your resume and provide the job description
                you want to target.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # INPUT COLUMNS
    # --------------------------------------------------------

    resume_column, jd_column = st.columns(
        2,
        gap="large",
    )


    # --------------------------------------------------------
    # RESUME
    # --------------------------------------------------------

    with resume_column:

        st.html(
            """
            <div class="section-card">

                <div class="info-title">
                    📄 Your Resume
                </div>

                <div class="info-content">
                    Upload your resume in PDF or DOCX format.
                </div>

            </div>
            """
        )


        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            key="resume_upload",
        )


        if uploaded_file is not None:

            st.success(
                f"✓ {uploaded_file.name} is ready for analysis."
            )


    # --------------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------------

    with jd_column:

        st.html(
            """
            <div class="section-card">

                <div class="info-title">
                    💼 Job Description
                </div>

                <div class="info-content">
                    Paste the job description for the role you're targeting.
                </div>

            </div>
            """
        )


        job_description = st.text_area(
            "Job description",
            height=280,
            placeholder="Paste the job description here...",
            key="job_description",
        )


    st.write("")


    # --------------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------------

    analyze_left, analyze_middle, analyze_right = st.columns(
        [1.5, 2, 1.5],
    )


    with analyze_middle:

        analyze_clicked = st.button(
            "Analyze Resume  →",
            key="analyze_resume_button",
            type="secondary",
            use_container_width=True,
        )


    if analyze_clicked:

        if uploaded_file is None:

            st.error(
                "Please upload your resume before starting the analysis."
            )

        elif not job_description.strip():

            st.error(
                "Please enter the job description before starting the analysis."
            )

        else:

            temporary_path = None

            try:

                file_suffix = Path(
                    uploaded_file.name
                ).suffix.lower()


                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=file_suffix,
                ) as temporary_file:

                    temporary_file.write(
                        uploaded_file.getbuffer()
                    )

                    temporary_path = temporary_file.name


                with st.spinner(
                    "Analyzing your resume against the job description..."
                ):

                    result = analyze_resume_file(
                        file_path=temporary_path,
                        job_description=job_description.strip(),
                        top_k=3,
                        chunk_size=500,
                    )


                st.session_state.analysis_result = result

                st.session_state.resume_data = uploaded_file.name

                st.session_state.job_description_data = (
                    job_description.strip()
                )


                if temporary_path is not None:

                    try:
                        Path(temporary_path).unlink(
                            missing_ok=True
                        )
                    except Exception:
                        pass


                st.session_state.current_page = "results"
                st.session_state.scroll_to_top = True

                st.rerun()


            except Exception as error:

                if temporary_path is not None:

                    try:
                        Path(temporary_path).unlink(
                            missing_ok=True
                        )
                    except Exception:
                        pass


                st.error(
                    "Something went wrong while analyzing the resume."
                )

                with st.expander("Technical details"):
                    st.code(str(error))


    # --------------------------------------------------------
    # TIP
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-card">

            <div class="info-content">
                💡 <strong>Tip:</strong>
                For the most useful analysis, use the complete
                job description rather than only the job title.
            </div>

        </div>
        """
    )


# ============================================================
# RESULTS PAGE
# ============================================================

elif st.session_state.current_page == "results":

    result = st.session_state.analysis_result


    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if result is None:

        st.html(
           """
           <div class="info-card">
                <div class="info-content">
                    Analyze a resume first to view results.
                </div>
           </div>
           """
        )

        if st.button(
            "Go to Analysis →",
            key="missing_result_button",
            type="secondary",
        ):
            navigate_to("analysis")

        st.stop()


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="page-header">

            <div class="page-label">
                Analysis Complete
            </div>

            <div class="page-title">
                Your Resume Match Results
            </div>

            <div class="page-description">
                Here's how your resume aligns with the job description.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # OVERALL MATCH
    # --------------------------------------------------------

    overall_score = float(
        result.get("overall_match", 0)
    )

    match_category = html.escape(
        str(result.get("match_category", "Match"))
    )


    st.html(
        f"""
        <div class="score-card">

            <div class="score-label">
                OVERALL MATCH
            </div>

            <div class="score-number">
                {overall_score:.1f}%
            </div>

            <div class="match-category">
                {match_category}
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # SKILL MATCH
    # --------------------------------------------------------

    st.html(
        """
        <div class="page-header">

            <div class="page-title">
                Skill Match
            </div>

            <div class="page-description">
                Skills identified from your resume and the job description.
            </div>

        </div>
        """
    )


    skill_score = result.get("skill_score")


    if skill_score is not None:

        skill_percentage = float(skill_score)

        st.html(
            f"""
            <div class="skill-card">

                <div class="skill-match-score">
                    {skill_percentage:.0f}%
                </div>

                <div class="info-content">
                    of the identified job-description skills
                    were found in your resume.
                </div>

            </div>
            """
        )

    else:

        st.info(
            "No recognizable skills were identified in the job description."
        )


    # --------------------------------------------------------
    # MATCHING / MISSING SKILLS
    # --------------------------------------------------------

    matching_skills = result.get(
        "matching_skills",
        [],
    )

    missing_skills = result.get(
        "missing_skills",
        [],
    )


    matching_column, missing_column = st.columns(
        2,
        gap="large",
    )


    with matching_column:

        st.html(
            """
            <div class="section-card">

                <div class="info-title">
                    ✓ Matching Skills
                </div>

                <div class="info-content">
                    Skills found in both your resume and the job description.
                </div>

            </div>
            """
        )


        if matching_skills:

            pills = "".join(
                f"""
                <span class="skill-pill">
                    {html.escape(str(skill))}
                </span>
                """
                for skill in matching_skills
            )

            st.html(pills)

        else:

            st.info(
                "No matching skills were identified."
            )


    with missing_column:

        st.html(
            """
            <div class="section-card">

                <div class="info-title">
                    ! Missing / Weak Skills
                </div>

                <div class="info-content">
                    Job-description skills that were not identified
                    in your resume.
                </div>

            </div>
            """
        )


        if missing_skills:

            pills = "".join(
                f"""
                <span class="missing-pill">
                    {html.escape(str(skill))}
                </span>
                """
                for skill in missing_skills
            )

            st.html(pills)

        else:

            st.success(
                "No missing skills were identified."
            )


    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    st.html(
        """
        <div class="page-header">

            <div class="page-title">
                Experience
            </div>

            <div class="page-description">
                Relevant experience information identified from your resume.
            </div>

        </div>
        """
    )


    experience = result.get(
        "relevant_experience",
        [],
    )


    if experience:

        experience_html = "".join(
            f"""
            <div class="info-card">

                <div class="info-content">
                    • {html.escape(str(item))}
                </div>

            </div>
            """
            for item in experience
        )

        st.html(experience_html)

    else:

        st.info(
            "No prior experience mentioned."
        )


    # --------------------------------------------------------
    # EDUCATION
    # --------------------------------------------------------

    st.html(
        """
        <div class="page-header">

            <div class="page-title">
                Education
            </div>

            <div class="page-description">
                Education information identified from your resume.
            </div>

        </div>
        """
    )


    education = html.escape(
        str(
            result.get(
                "education_alignment",
                "No education information was identified in the resume.",
            )
        )
    )


    st.html(
        f"""
        <div class="info-card">

            <div class="info-title">
                🎓 Education
            </div>

            <div class="info-content">
                {education}
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = result.get(
        "recommendations",
        [],
    )


    st.html(
        """
        <div class="page-header">

            <div class="page-title">
                Recommendations
            </div>

            <div class="page-description">
                Suggestions based on your resume and the target job.
            </div>

        </div>
        """
    )


    if recommendations:

        recommendation_html = "".join(
            f"""
            <div class="recommendation">
                {html.escape(str(recommendation))}
            </div>
            """
            for recommendation in recommendations
        )

        st.html(recommendation_html)

    else:

        st.info(
            "No additional recommendations were generated."
        )


    # ========================================================
    # BOTTOM ACTIONS
    # ========================================================

    st.write("")
    st.write("")


    bottom_left, bottom_middle, bottom_right = st.columns(
        [1.5, 2, 1.5],
    )


    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    with bottom_left:

        if st.button(
            "← Go to Home",
            key="result_home_button",
            type="secondary",
            use_container_width=True,
        ):
            navigate_to("home")


    # --------------------------------------------------------
    # NEW RESUME
    # --------------------------------------------------------

    with bottom_right:

        if st.button(
            "Try Another Resume →",
            key="result_new_analysis_button",
            type="secondary",
            use_container_width=True,
        ):
            start_new_analysis()


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        🤖 ResumeMatch AI
        <br>
        AI-powered resume and job matching assistant
    </div>
    """
)