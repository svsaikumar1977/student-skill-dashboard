import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Student Digital Skill Assessment",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# SUPABASE CONNECTION
# --------------------------------------------------

@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🎓 Skill Assessment")

page = st.sidebar.radio(
    "Navigation",
    ["📝 Student Assessment", "📊 Dashboard"]
)

# ==================================================
# STUDENT ASSESSMENT
# ==================================================

if page == "📝 Student Assessment":

    st.title("🎓 Student Digital Skill Assessment")

    st.write(
        "This short assessment helps us understand students' "
        "digital skills and identify suitable training programs."
    )

    st.info("⏱️ Approximate completion time: 2–3 minutes")

    with st.form("skill_assessment_form"):

        st.subheader("👤 Student Information")

        student_id = st.text_input(
            "Student ID / Roll Number *"
        )

        student_name = st.text_input(
            "Student Name *"
        )

        program = st.selectbox(
            "Program *",
            [
                "Select",
                "B.Pharm",
                "Pharm.D",
                "M.Pharm"
            ]
        )

        study_year = st.selectbox(
            "Year of Study *",
            [
                "Select",
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year",
                "5th Year",
                "6th Year"
            ]
        )

        gender = st.selectbox(
            "Gender",
            [
                "Select",
                "Male",
                "Female",
                "Prefer not to say"
            ]
        )

        st.divider()

        # -------------------------------------------
        # DIGITAL SKILLS
        # -------------------------------------------

        st.subheader("💻 Digital Skills")

        st.write(
            "Rate your present skill level from "
            "**1 (Beginner) to 5 (Advanced).**"
        )

        excel_skill = st.slider(
            "Excel / Spreadsheet Skills",
            1,
            5,
            1
        )

        python_skill = st.slider(
            "Python Programming",
            1,
            5,
            1
        )

        data_analysis_skill = st.slider(
            "Data Analysis",
            1,
            5,
            1
        )

        ai_tools_skill = st.slider(
            "AI Tools (ChatGPT, Gemini, etc.)",
            1,
            5,
            1
        )

        programming_experience = st.radio(
            "Previous programming experience?",
            ["No", "Yes"],
            horizontal=True
        )

        st.divider()

        # -------------------------------------------
        # TRAINING INTEREST
        # -------------------------------------------

        st.subheader("🎯 Training Interests")

        training_interest = st.multiselect(
            "Which areas would you like to learn?",
            [
                "Excel & Data Analysis",
                "Python Programming",
                "Artificial Intelligence",
                "Machine Learning",
                "Research Data Analysis",
                "Dashboard Development",
                "AI Applications in Pharmacy"
            ]
        )

        willing_for_training = st.radio(
            "Would you participate in a digital skills training program?",
            ["Yes", "Maybe", "No"],
            horizontal=True
        )

        comments = st.text_area(
            "Additional comments / expectations (Optional)"
        )

        submitted = st.form_submit_button(
            "Submit Assessment",
            use_container_width=True
        )

    # -----------------------------------------------
    # PROCESS SUBMISSION
    # -----------------------------------------------

    if submitted:

        if (
            not student_id.strip()
            or not student_name.strip()
            or program == "Select"
            or study_year == "Select"
        ):

            st.error(
                "⚠️ Please complete Student ID, Name, "
                "Program and Year of Study."
            )

        else:

            # Calculate readiness score

            total_skill_score = (
                excel_skill
                + python_skill
                + data_analysis_skill
                + ai_tools_skill
            )

            readiness_score = (
                total_skill_score / 20
            ) * 100

            # Determine readiness level

            if readiness_score < 40:
                readiness_level = "Beginner"

            elif readiness_score < 60:
                readiness_level = "Developing"

            elif readiness_score < 80:
                readiness_level = "Ready"

            else:
                readiness_level = "Advanced"

            # Convert multiple selections to text

            training_text = ", ".join(training_interest)

            # Data sent to Supabase

            response_data = {

                "student_id":
                    student_id.strip(),

                "student_name":
                    student_name.strip(),

                "program":
                    program,

                "study_year":
                    study_year,

                "gender":
                    gender,

                "excel_skill":
                    excel_skill,

                "python_skill":
                    python_skill,

                "data_analysis_skill":
                    data_analysis_skill,

                "ai_tools_skill":
                    ai_tools_skill,

                "programming_experience":
                    programming_experience,

                "training_interest":
                    training_text,

                "willing_for_training":
                    willing_for_training,

                "comments":
                    comments,

                "readiness_score":
                    readiness_score,

                "readiness_level":
                    readiness_level
            }

            try:

                supabase.table(
                    "student_responses"
                ).insert(
                    response_data
                ).execute()

                st.success(
                    "✅ Assessment submitted successfully!"
                )

                st.subheader(
                    "Your Digital Skill Readiness"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Readiness Score",
                        f"{readiness_score:.0f}%"
                    )

                with col2:

                    st.metric(
                        "Readiness Level",
                        readiness_level
                    )

                st.progress(
                    int(readiness_score)
                )

                if readiness_score < 40:

                    st.info(
                        "Recommended starting point: "
                        "Digital fundamentals, Excel and "
                        "basic data handling."
                    )

                elif readiness_score < 60:

                    st.info(
                        "Recommended next step: "
                        "Python fundamentals and practical "
                        "data-analysis exercises."
                    )

                elif readiness_score < 80:

                    st.info(
                        "Recommended next step: "
                        "Applied Python, dashboards and "
                        "AI-assisted data analysis."
                    )

                else:

                    st.info(
                        "Recommended next step: "
                        "Advanced analytics, machine learning "
                        "and application development."
                    )

            except Exception as e:

                st.error(
                    "❌ Submission could not be saved."
                )

                st.code(str(e))


# ==================================================
# DASHBOARD
# ==================================================

elif page == "📊 Dashboard":

    st.title("📊 Student Digital Skills Dashboard")

    st.write(
        "Live analysis of responses collected through "
        "the Student Skill Assessment."
    )

    # -----------------------------------------------
    # LOAD DATA
    # -----------------------------------------------

    try:

        response = (
            supabase
            .table("student_responses")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        data = response.data

        if not data:

            st.warning(
                "No student responses have been submitted yet."
            )

            st.stop()

        df = pd.DataFrame(data)

    except Exception as e:

        st.error(
            "Unable to retrieve dashboard data."
        )

        st.code(str(e))

        st.stop()

    # -----------------------------------------------
    # DASHBOARD FILTERS
    # -----------------------------------------------

    st.subheader("🔎 Filters")

    filter1, filter2 = st.columns(2)

    with filter1:

        program_options = [
            "All"
        ] + sorted(
            df["program"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_program = st.selectbox(
            "Program",
            program_options
        )

    with filter2:

        year_options = [
            "All"
        ] + sorted(
            df["study_year"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_year = st.selectbox(
            "Year",
            year_options
        )

    filtered_df = df.copy()

    if selected_program != "All":

        filtered_df = filtered_df[
            filtered_df["program"]
            == selected_program
        ]

    if selected_year != "All":

        filtered_df = filtered_df[
            filtered_df["study_year"]
            == selected_year
        ]

    if filtered_df.empty:

        st.warning(
            "No responses match the selected filters."
        )

        st.stop()

    st.divider()

    # -----------------------------------------------
    # KPI CARDS
    # -----------------------------------------------

    total_responses = len(filtered_df)

    average_readiness = (
        filtered_df["readiness_score"]
        .astype(float)
        .mean()
    )

    python_average = (
        filtered_df["python_skill"]
        .astype(float)
        .mean()
    )

    ai_average = (
        filtered_df["ai_tools_skill"]
        .astype(float)
        .mean()
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Students",
        total_responses
    )

    kpi2.metric(
        "Avg. Readiness",
        f"{average_readiness:.1f}%"
    )

    kpi3.metric(
        "Avg. Python Skill",
        f"{python_average:.1f}/5"
    )

    kpi4.metric(
        "Avg. AI Skill",
        f"{ai_average:.1f}/5"
    )

    st.divider()

    # -----------------------------------------------
    # AVERAGE SKILLS
    # -----------------------------------------------

    st.subheader(
        "📚 Average Digital Skill Levels"
    )

    skill_columns = {

        "Excel":
            "excel_skill",

        "Python":
            "python_skill",

        "Data Analysis":
            "data_analysis_skill",

        "AI Tools":
            "ai_tools_skill"
    }

    skill_average = {}

    for skill_name, column_name in skill_columns.items():

        skill_average[skill_name] = (
            filtered_df[column_name]
            .astype(float)
            .mean()
        )

    skill_df = pd.DataFrame({

        "Skill":
            list(skill_average.keys()),

        "Average Score":
            list(skill_average.values())
    })

    st.bar_chart(
        skill_df.set_index("Skill")
    )

    # -----------------------------------------------
    # READINESS DISTRIBUTION
    # -----------------------------------------------

    st.subheader(
        "🎯 Digital Readiness Distribution"
    )

    readiness_counts = (
        filtered_df[
            "readiness_level"
        ]
        .value_counts()
    )

    st.bar_chart(
        readiness_counts
    )

    # -----------------------------------------------
    # PROGRAM DISTRIBUTION
    # -----------------------------------------------

    st.subheader(
        "🎓 Responses by Program"
    )

    program_counts = (
        filtered_df[
            "program"
        ]
        .value_counts()
    )

    st.bar_chart(
        program_counts
    )

    # -----------------------------------------------
    # TRAINING WILLINGNESS
    # -----------------------------------------------

    st.subheader(
        "🙋 Willingness for Training"
    )

    willingness_counts = (
        filtered_df[
            "willing_for_training"
        ]
        .value_counts()
    )

    st.bar_chart(
        willingness_counts
    )

    # -----------------------------------------------
    # TRAINING INTEREST ANALYSIS
    # -----------------------------------------------

    st.subheader(
        "🚀 Preferred Training Areas"
    )

    interests = []

    for value in filtered_df[
        "training_interest"
    ].dropna():

        if value:

            interests.extend(
                [
                    item.strip()
                    for item in value.split(",")
                ]
            )

    if interests:

        interest_df = pd.Series(
            interests
        ).value_counts()

        st.bar_chart(
            interest_df
        )

    else:

        st.info(
            "No training interests have been selected yet."
        )

    # -----------------------------------------------
    # IDENTIFY TRAINING PRIORITY
    # -----------------------------------------------

    st.subheader(
        "🧭 Training Priority Analysis"
    )

    weakest_skill = min(
        skill_average,
        key=skill_average.get
    )

    strongest_skill = max(
        skill_average,
        key=skill_average.get
    )

    colA, colB = st.columns(2)

    with colA:

        st.warning(
            f"Priority Training Area: "
            f"**{weakest_skill}** "
            f"({skill_average[weakest_skill]:.2f}/5)"
        )

    with colB:

        st.success(
            f"Strongest Current Area: "
            f"**{strongest_skill}** "
            f"({skill_average[strongest_skill]:.2f}/5)"
        )

    # -----------------------------------------------
    # RESPONSE DATA
    # -----------------------------------------------

    st.subheader(
        "📋 Response Data"
    )

    display_columns = [

        "student_id",
        "student_name",
        "program",
        "study_year",
        "excel_skill",
        "python_skill",
        "data_analysis_skill",
        "ai_tools_skill",
        "readiness_score",
        "readiness_level",
        "willing_for_training"
    ]

    st.dataframe(
        filtered_df[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------

    csv = (
        filtered_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "⬇️ Download Filtered Data",
        csv,
        "student_skill_responses.csv",
        "text/csv",
        use_container_width=True
    )