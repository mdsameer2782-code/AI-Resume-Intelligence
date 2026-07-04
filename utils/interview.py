from utils.llm import generate

def generate_interview_questions(resume_text, job_text):
    prompt = f"""
You are an AI interviewer.

Resume:
{resume_text}

Job Description:
{job_text}

Generate:

1. Five Python interview questions.
2. Five Machine Learning interview questions.
3. Five Deep Learning interview questions.
4. Five SQL interview questions.
5. Five HR interview questions.
6. Five project-based interview questions.

Return only the questions.
"""

    return generate(prompt)