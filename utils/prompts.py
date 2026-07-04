PROMPT = """
You are an expert ATS Resume Reviewer.

Compare the resume with the job description.

Resume:
{resume}

Job Description:
{job}

Generate:

1. ATS Score (0-100)
2. Resume Match Score
3. Strengths
4. Weaknesses
5. Missing Skills
6. Resume Summary
7. Suggestions for Improvement

Return the response in a clear, professional format.
"""