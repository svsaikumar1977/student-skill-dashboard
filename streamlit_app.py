import streamlit as st
import pandas as pd
from supabase import create_client

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Digital Skill Assessment",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# SUPABASE CONNECTION
# =========================================================

@st.cache_resource
def init_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = init_supabase()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def calculate_readiness(excel, python, data_analysis, ai):
    total = excel + python + data_analysis + ai
    score = (total / 20) * 100

    if score < 40:
        level = "Beginner"
    elif score < 60:
        level = "Developing"
    elif score < 80:
        level = "Ready"
    else:
        level = "Advanced"

    return score, level


def student_exists(student_id):

    result = (
        supabase
        .table("student_responses")
        .select("student_id")
        .eq("student_id", student_id.strip())
        .execute()
    )

    return len(result.data) > 0


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎓 Digital Skills")

page = st.sidebar.radio(
    "Select",
    [
        "📝 Skill Assessment",
        "🔐 Faculty Dashboard"
    ]
)


# =========================================================
# STUDENT ASSESSMENT
# =========================================================

if page == "📝 Skill Assessment":

    st.title("🎓 Student Digital Skill Assessment")

    st.write(
        "This short assessment helps identify students' "
        "current digital skills and future training needs."
    )

    st.info("⏱️ Approximate completion time: 2–3 minutes")

    with st.form("student_form"):

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

        # -------------------------------------------------
        # DIGITAL SKILLS
        # -------------------------------------------------

        st.subheader("💻 Digital Skills")

        st.caption(
            "Rate your present skill level: "
            "1 = Beginner and 5 = Advanced"
        )

        excel_skill = st.slider(
            "Excel / Spreadsheet Skills",
            1, 5, 1
        )

        python_skill = st.slider(
            "Python Programming",
            1, 5, 1
        )

        data_analysis_skill = st.slider(
            "Data Analysis",
            1, 5, 1
        )

        ai_tools_skill = st.slider(
            "AI Tools (ChatGPT, Gemini, etc.)",
            1, 5, 1
        )

        programming_experience = st.radio(
            "Previous programming experience?",
            ["No", "Yes"],
            horizontal=True
        )

        st.divider()

        # -------------------------------------------------
        # TRAINING NEEDS
        # -------------------------------------------------

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
            "Comments / expectations (Optional)"
        )

        submitted = st.form_submit_button(
            "Submit Assessment",
            use_container_width=True
        )

    # =====================================================
    # PROCESS SUBMISSION
    # =====================================================

    if submitted:

        clean_id = student_id.strip()

        if (
            not clean_id
            or not student_name.strip()
            or program == "Select"
            or study_year == "Select"
        ):

            st.error(
                "⚠️ Please complete Student ID, Name, "
                "Program and Year."
            )

        else:

            try:

                # -----------------------------------------
                # DUPLICATE CHECK
                # -----------------------------------------

                if student_exists(clean_id):

                    st.warning(
                        "⚠️ A response has already been "
                        "submitted for this Student ID."
                    )

                    st.info(
                        "If you believe this is an error, "
                        "please contact the faculty coordinator."
                    )

                else:

                    readiness_score, readiness_level = (
                        calculate_readiness(
                            excel_skill,
                            python_skill,
                            data_analysis_skill,
                            ai_tools_skill
                        )
                    )

                    response_data = {

                        "student_id":
                            clean_id,

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
                            ", ".join(training_interest),

                        "willing_for_training":
                            willing_for_training,

                        "comments":
                            comments,

                        "readiness_score":
                            readiness_score,

                        "readiness_level":
                            readiness_level
                    }

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

                    c1, c2 = st.columns(2)

                    c1.metric(
                        "Readiness Score",
                        f"{readiness_score:.0f}%"
                    )

                    c2.metric(
                        "Readiness Level",
                        readiness_level
                    )

                    st.progress(
                        int(readiness_score)
                    )

                    if readiness_level == "Beginner":

                        st.info(
                            "Suggested starting point: "
                            "Excel, digital fundamentals and "
                            "basic data handling."
                        )

                    elif readiness_level == "Developing":

                        st.info(
                            "Suggested next step: "
                            "Python fundamentals and practical "
                            "data analysis."
                        )

                    elif readiness_level == "Ready":

                        st.info(
                            "Suggested next step: "
                            "Applied Python, dashboards and "
                            "AI-assisted analysis."
                        )

                    else:

                        st.info(
                            "Suggested next step: "
                            "Machine learning, advanced analytics "
                            "and application development."
                        )

            except Exception as e:

                st.error(
                    "❌ Something went wrong while "
                    "processing the submission."
                )

                st.code(str(e))


# =========================================================
# FACULTY DASHBOARD LOGIN
# =========================================================

elif page == "🔐 Faculty Dashboard":

    st.title("🔐 Faculty Dashboard")

    # Initialize authentication state

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    if not st.session_state.admin_authenticated:

        st.write(
            "Faculty authorization is required "
            "to access individual student data."
        )

        password = st.text_input(
            "Faculty Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if password == st.secrets["ADMIN_PASSWORD"]:

                st.session_state.admin_authenticated = True
                st.rerun()

            else:

                st.error(
                    "Incorrect password."
                )

        st.stop()

    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    top1, top2 = st.columns(
        [5, 1]
    )

    with top1:

        st.success(
            "Faculty dashboard access granted."
        )

    with top2:

        if st.button("Logout"):

            st.session_state.admin_authenticated = False
            st.rerun()

    # =====================================================
    # LOAD DATA
    # =====================================================

    try:

        response = (
            supabase
            .table("student_responses")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        df = pd.DataFrame(
            response.data
        )

    except Exception as e:

        st.error(
            "Unable to retrieve dashboard data."
        )

        st.code(str(e))
        st.stop()

    if df.empty:

        st.warning(
            "No responses have been submitted yet."
        )

        st.stop()

    # =====================================================
    # FILTERS
    # =====================================================

    st.subheader("🔎 Analyse Students")

    f1, f2 = st.columns(2)

    with f1:

        program_options = (
            ["All"]
            + sorted(
                df["program"]
                .dropna()
                .unique()
                .tolist()
            )
        )

        selected_program = st.selectbox(
            "Program",
            program_options
        )

    with f2:

        year_options = (
            ["All"]
            + sorted(
                df["study_year"]
                .dropna()
                .unique()
                .tolist()
            )
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
            "No responses match these filters."
        )

        st.stop()

    # =====================================================
    # KPIs
    # =====================================================

    st.divider()

    total_students = len(
        filtered_df
    )

    average_readiness = (
        filtered_df["readiness_score"]
        .astype(float)
        .mean()
    )

    beginner_developing = (
        filtered_df[
            "readiness_level"
        ]
        .isin(
            ["Beginner", "Developing"]
        )
        .mean()
        * 100
    )

    training_interest_rate = (
        filtered_df[
            "willing_for_training"
        ]
        .isin(
            ["Yes", "Maybe"]
        )
        .mean()
        * 100
    )

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Students",
        total_students
    )

    k2.metric(
        "Average Readiness",
        f"{average_readiness:.1f}%"
    )

    k3.metric(
        "Need Foundation Training",
        f"{beginner_developing:.1f}%"
    )

    k4.metric(
        "Training Interest",
        f"{training_interest_rate:.1f}%"
    )

    # =====================================================
    # SKILL GAP ANALYSIS
    # =====================================================

    st.divider()

    st.subheader(
        "📊 Skill Gap Analysis"
    )

    skills = {

        "Excel":
            "excel_skill",

        "Python":
            "python_skill",

        "Data Analysis":
            "data_analysis_skill",

        "AI Tools":
            "ai_tools_skill"
    }

    skill_scores = {}

    for skill, column in skills.items():

        skill_scores[skill] = (
            filtered_df[column]
            .astype(float)
            .mean()
        )

    skill_df = pd.DataFrame(
        {
            "Skill":
                skill_scores.keys(),

            "Average Score":
                skill_scores.values()
        }
    )

    st.bar_chart(
        skill_df.set_index("Skill")
    )

    weakest_skill = min(
        skill_scores,
        key=skill_scores.get
    )

    strongest_skill = max(
        skill_scores,
        key=skill_scores.get
    )

    c1, c2 = st.columns(2)

    c1.warning(
        f"Priority Training Area: "
        f"**{weakest_skill}** "
        f"({skill_scores[weakest_skill]:.2f}/5)"
    )

    c2.success(
        f"Strongest Skill Area: "
        f"**{strongest_skill}** "
        f"({skill_scores[strongest_skill]:.2f}/5)"
    )

    # =====================================================
    # READINESS DISTRIBUTION
    # =====================================================

    st.subheader(
        "🎯 Readiness Distribution"
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

    # =====================================================
    # TRAINING DEMAND
    # =====================================================

    st.subheader(
        "🚀 Training Demand"
    )

    interests = []

    for entry in (
        filtered_df[
            "training_interest"
        ]
        .dropna()
    ):

        if entry:

            interests.extend(
                [
                    x.strip()
                    for x in entry.split(",")
                ]
            )

    if interests:

        interest_counts = (
            pd.Series(interests)
            .value_counts()
        )

        st.bar_chart(
            interest_counts
        )

        top_interest = (
            interest_counts
            .index[0]
        )

        st.info(
            f"Most requested training area: "
            f"**{top_interest}**"
        )

    # =====================================================
    # STUDENT DATA
    # =====================================================

    st.divider()

    st.subheader(
        "📋 Individual Student Data"
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

    # =====================================================
    # DOWNLOAD
    # =====================================================

    csv = (
        filtered_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "⬇️ Download Filtered Dataset",
        csv,
        "student_skill_assessment.csv",
        "text/csv",
        use_container_width=True
    )