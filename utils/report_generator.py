from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    filename,
    score,
    matched,
    missing,
    summary,
    cover_letter,
    interview_questions,
):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>AI Resume Intelligence Report</b>", styles["Title"]))

    elements.append(Paragraph(f"<b>ATS Score:</b> {score}%", styles["Heading2"]))

    elements.append(
        Paragraph(
            "<b>Matched Skills:</b><br/>" + "<br/>".join(matched),
            styles["BodyText"],
        )
    )

    elements.append(
        Paragraph(
            "<b>Missing Skills:</b><br/>" + "<br/>".join(missing),
            styles["BodyText"],
        )
    )

    elements.append(Paragraph("<b>Resume Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(summary.replace("\n", "<br/>"), styles["BodyText"]))

    elements.append(Paragraph("<b>Cover Letter</b>", styles["Heading2"]))
    elements.append(
        Paragraph(cover_letter.replace("\n", "<br/>"), styles["BodyText"])
    )

    elements.append(Paragraph("<b>Interview Questions</b>", styles["Heading2"]))
    elements.append(
        Paragraph(interview_questions.replace("\n", "<br/>"), styles["BodyText"])
    )

    doc.build(elements)