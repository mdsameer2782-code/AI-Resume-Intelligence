from utils.llm import generate

def generate_cover_letter(resume_text, job_text):
    prompt = f"""
Write a professional cover letter.

Resume:
{resume_text}

Job Description:
{job_text}

The cover letter should:
- Be professional.
- Highlight relevant skills.
- Be around 250 words.
"""

    return generate(prompt)