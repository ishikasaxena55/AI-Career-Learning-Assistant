import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# ==========================
# GROQ API KEY
# ==========================

API_KEY = "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"

client = Groq(api_key=API_KEY)

# ==========================
# ATS SCORE FUNCTION
# ==========================

def calculate_ats_score(resume_text):
    keywords = [
        "python",
        "sql",
        "git",
        "flask",
        "django",
        "api",
        "docker",
        "aws"
    ]

    found = [k for k in keywords if k in resume_text.lower()]
    score = int((len(found) / len(keywords)) * 100)

    missing = list(set(keywords) - set(found))

    return score, missing

# ==========================
# UI
# ==========================

st.title("AI Career & Learning Assistant 🚀")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_role = st.text_input(
    "Enter Target Job Role"
)

resume_text = ""

# ==========================
# PDF READING
# ==========================

if uploaded_file:

    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    st.success("Resume uploaded successfully!")

# ==========================
# ANALYZE BUTTON
# ==========================

if st.button("Analyze Resume"):

    if not uploaded_file:
        st.warning("Please upload resume first.")
        st.stop()

    if not job_role:
        st.warning("Please enter target role.")
        st.stop()

    score, missing_skills = calculate_ats_score(resume_text)

    try:

        prompt = f"""
You are a career advisor.

Analyze this resume for the role of {job_role}.

Resume:
{resume_text}

Give:

1. Resume Summary
2. Strengths
3. Weaknesses
4. Missing Skills
5. Improvement Suggestions
6. Learning Roadmap
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        ai_report = response.choices[0].message.content

        st.success("Analysis Completed Successfully!")

        st.subheader("AI Analysis")
        st.write(ai_report)

    except Exception as e:

        ai_report = f"""
AI analysis unavailable.

ATS Score: {score}/100

Missing Skills:
{', '.join(missing_skills)}

Recommended Skills:
- Flask
- Django
- AWS
- Docker
"""

        st.warning("AI API unavailable. Showing ATS report only.")

    # ==========================
    # ATS SCORE
    # ==========================

    st.subheader("ATS Score")

    st.metric(
        "Score",
        f"{score}/100"
    )

    st.progress(score)

    st.subheader("Missing Skills")

    for skill in missing_skills:
        st.write("❌", skill)

    # ==========================
    # DOWNLOAD REPORT
    # ==========================

    report = f"""
AI CAREER REPORT

Target Role: {job_role}

ATS Score: {score}/100

Missing Skills:
{', '.join(missing_skills)}

AI Analysis:

{ai_report}
"""

    st.download_button(
        label="Download Report",
        data=report,
        file_name="career_report.txt",
        mime="text/plain"
    )