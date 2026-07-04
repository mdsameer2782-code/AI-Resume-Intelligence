import re

def extract_skills(text):
    skills = [
        "python", "machine learning", "deep learning", "langchain",
        "hugging face", "fastapi", "docker", "aws", "sql",
        "git", "github", "pandas", "numpy", "scikit-learn",
        "tensorflow", "pytorch", "faiss", "rest api"
    ]

    text = text.lower()

    found = []

    for skill in skills:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)

    return list(set(found))


def compare_resume_job(resume_text, job_text):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = list(set(resume_skills) & set(job_skills))

    missing = list(set(job_skills) - set(resume_skills))

    if len(job_skills) == 0:
        score = 0
    else:
        score = int((len(matched) / len(job_skills)) * 100)

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }