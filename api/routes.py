from fastapi import APIRouter, UploadFile, File
import shutil
import os

from utils.pdf_loader import extract_text
from utils.scoring import compare_resume_job
from utils.llm import generate
from utils.cover_letter import generate_cover_letter
from utils.interview import generate_interview_questions
from utils.report_generator import generate_report
from fastapi.responses import FileResponse


# RAG Imports
from utils.embeddings import get_embeddings
from utils.rag import create_vector_store,load_vector_store

router = APIRouter()

# Global Vector Store
vector_store = None


@router.post("/api/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job: UploadFile = File(...)
):

    os.makedirs("data", exist_ok=True)

    resume_path = f"data/{resume.filename}"
    job_path = f"data/{job.filename}"

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    with open(job_path, "wb") as buffer:
        shutil.copyfileobj(job.file, buffer)

    resume_text = extract_text(resume_path)
    job_text = extract_text(job_path)

    # Build Vector Store
    global vector_store
    embeddings = get_embeddings()

    vector_store = load_vector_store(embeddings)
    if vector_store is None:
        vector_store = create_vector_store(resume_text,embeddings)

    result = compare_resume_job(resume_text, job_text)

    prompt = f"""
ATS Score: {result['score']}

Matched Skills:
{', '.join(result['matched'])}

Missing Skills:
{', '.join(result['missing'])}

Write a professional resume summary.
"""

    result["summary"] = generate(prompt)

    result["cover_letter"] = generate_cover_letter(
        resume_text,
        job_text
    )

    result["interview_questions"] = generate_interview_questions(
        resume_text,
        job_text
    )

    report_path = "ATS_Report,pdf"

    generate_report(
        report_path,
        result["score"],
        result["matched"],
        result["missing"],
        result["summary"],
        result["cover_letter"],
        result["interview_questions"],
    )
    suggestions = []

    if "tensorflow" in result["missing"]:
        suggestions.append("Learn and add TensorFlow projects.")

    if "docker" in result["missing"]:
        suggestions.append("Mention Docker deployment experience.")

    if "aws" in result["missing"]:
        suggestions.append("Add AWS cloud deployment skills.")

    if len(result["matched"]) < 10:
        suggestions.append("Include more AI/ML tools in your resume.")

    suggestions.append("Quantify your achievements using numbers.")

    suggestions.append("Add GitHub project links.")

    result["suggestions"] = suggestions


    return result



@router.get("/download-report")
async def download_report():
    return FileResponse(
        "ATS_Report.pdf",
        media_type="application/pdf",
        filename="ATS_Report.pdf"
    )