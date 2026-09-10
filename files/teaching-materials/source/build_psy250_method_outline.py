#!/usr/bin/env python3
"""Build the PSY 250 Method Outline teaching-portfolio handout."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "PSY250_Method_Outline_Assignment_and_Rubric.pdf"

pdfmetrics.registerFont(TTFont("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Bold", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Italic", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"))


class PortfolioDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=letter, leftMargin=.68*inch, rightMargin=.68*inch,
                         topMargin=.62*inch, bottomMargin=.62*inch)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates(PageTemplate(id="all", frames=frame, onPage=self.footer))

    def footer(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#B8B8B8"))
        canvas.setLineWidth(.35)
        canvas.line(self.leftMargin, .43*inch, letter[0]-self.rightMargin, .43*inch)
        canvas.setFont("Georgia", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(self.leftMargin, .26*inch,
                          "PSY 250 Research Design & Analysis I  |  Summer 2026  |  Yiqing \u201cSkylar\u201d Yu")
        canvas.drawRightString(letter[0]-self.rightMargin, .26*inch, f"Page {doc.page}")
        canvas.restoreState()


def make_styles():
    getSampleStyleSheet()
    return {
        "meta": ParagraphStyle("meta", fontName="Georgia", fontSize=9, leading=12,
                               alignment=TA_CENTER, textColor=colors.HexColor("#3F3F3F"), spaceAfter=2),
        "title": ParagraphStyle("title", fontName="Georgia-Bold", fontSize=21, leading=24,
                                alignment=TA_CENTER, spaceAfter=2),
        "subtitle": ParagraphStyle("subtitle", fontName="Georgia", fontSize=13, leading=16,
                                   alignment=TA_CENTER, spaceAfter=14),
        "context": ParagraphStyle("context", fontName="Georgia-Italic", fontSize=8.6, leading=12,
                                  leftIndent=8, rightIndent=8,
                                  spaceAfter=13),
        "h1": ParagraphStyle("h1", fontName="Georgia-Bold", fontSize=14, leading=17,
                             spaceBefore=6, spaceAfter=7, keepWithNext=True),
        "h2": ParagraphStyle("h2", fontName="Georgia-Bold", fontSize=11, leading=14,
                             spaceBefore=7, spaceAfter=4, keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Georgia", fontSize=9.2, leading=13, spaceAfter=7),
        "callout": ParagraphStyle("callout", fontName="Georgia", fontSize=8.8, leading=12,
                                  leftIndent=8, rightIndent=8, spaceBefore=5, spaceAfter=9),
        "gradingnote": ParagraphStyle("gradingnote", fontName="Georgia-Italic", fontSize=8.8,
                                      leading=12.5, leftIndent=8, rightIndent=8,
                                      textColor=colors.HexColor("#3F3F3F"), spaceBefore=14),
        "bullet": ParagraphStyle("bullet", fontName="Georgia", fontSize=9.1, leading=12.5,
                                 leftIndent=21, firstLineIndent=-10, bulletIndent=8, spaceAfter=3),
        "small": ParagraphStyle("small", fontName="Georgia", fontSize=8.4, leading=11.5),
        "smallb": ParagraphStyle("smallb", fontName="Georgia-Bold", fontSize=8.4, leading=11.5),
    }


def rubric_table(s):
    rows = [
        [Paragraph("Criterion", s["smallb"]), Paragraph("Description", s["smallb"]), Paragraph("Points", s["smallb"])],
        [Paragraph("Participants", s["smallb"]),
         Paragraph("All requirements listed in the participant section of the assignment are met.", s["small"]),
         Paragraph("4", s["smallb"])],
        [Paragraph("Measures / Apparatus", s["smallb"]),
         Paragraph("All requirements listed in the measures/apparatus section of the assignment are met.", s["small"]),
         Paragraph("3", s["smallb"])],
        [Paragraph("Procedures", s["smallb"]),
         Paragraph("All requirements listed in the procedures section of the assignment are met.", s["small"]),
         Paragraph("3", s["smallb"])],
        [Paragraph("Total", s["smallb"]), Paragraph("", s["small"]), Paragraph("10", s["smallb"])],
    ]
    t = Table(rows, colWidths=[1.55*inch, 4.65*inch, .65*inch], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), .45, colors.HexColor("#A9A9A9")),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E5E5E5")),
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#F1F1F1")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (-1,0), (-1,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    return t


def build():
    s = make_styles()
    story = [
        Paragraph("Yiqing \u201cSkylar\u201d Yu", s["meta"]),
        Paragraph("PSY 250 Research Design & Analysis I", s["meta"]),
        Paragraph("Summer 2026", s["meta"]),
        Spacer(1, 7),
        Paragraph("Method Outline", s["title"]),
        Paragraph("Assignment & Rubric", s["subtitle"]),
        Paragraph("<b>Portfolio context:</b> This assignment is an intermediate scaffold in the semester-long research proposal project. Students use feedback from earlier study-design assignments to organize the participants, measures/apparatus, and procedure sections before drafting the full Method section.", s["context"]),
        Paragraph("Assignment Overview", s["h1"]),
        Paragraph("<b>Point value:</b> 10 points", s["body"]),
        Paragraph("Make sure you watch the lecture before starting this assignment: <u>Lecture: Writing a Method Section</u>.", s["body"]),
        Paragraph("<b>Instructions:</b> This is an outline of the method section for your final paper. At this point, you have received multiple rounds of feedback for your study design. If you haven't already, please carefully review your past assignments related to your study proposal before proceeding. In this assignment, use bullet points or brief phrases (not full sentences), but enough information to show you have the correct information there. Please use the template below to fill in each section and submit a doc or pdf file.", s["body"]),
        Paragraph("1. Participants", s["h2"]),
    ]
    for x in ["Total number of participants", "Recruitment source", "Compensation", "Exclusionary criteria", "Relevant demographic details", "Ethical considerations"]:
        story.append(Paragraph(x, s["bullet"], bulletText="\u2022"))
    story.append(Paragraph("2. Measures / Apparatus", s["h2"]))
    for x in ["Dependent variable (construct being measured) - Name of measure(s) & citation(s) for measure(s)",
              "Apparatus or materials used",
              "Additional measures (if applicable) - Name of measure(s) & citation(s) for measure(s)"]:
        story.append(Paragraph(x, s["bullet"], bulletText="\u2022"))
    story.append(Paragraph("3. Procedures", s["h2"]))
    for x in ["Study design (between-subjects, within-subjects, or mixed)", "Counterbalancing (if applicable)",
              "Step-by-step procedure (participant experience from start to finish)"]:
        story.append(Paragraph(x, s["bullet"], bulletText="\u2022"))
    story += [
        Paragraph("Academic Integrity and Generative AI", s["h2"]),
        Paragraph("All assignments must be written in <b>your own words</b>. <b>Using generative AI to write your assignment is considered plagiarism</b> and may be reported to the university as academic misconduct, as stated in the syllabus. Please avoid creating any issues around this by doing your own writing and using the course materials, feedback, and sample paper as guidance.", s["callout"]),
        PageBreak(),
        Paragraph("Method Outline Rubric", s["title"]),
        Paragraph("Total: 10 points", s["subtitle"]),
        rubric_table(s),
        Paragraph("<b>Grading note:</b> This assignment is evaluated primarily on completion of the required elements rather than on whether each response is fully polished or final. Its purpose is to provide formative feedback and guidance while students develop the outline for their Method section.", s["gradingnote"]),
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PortfolioDoc(str(OUTPUT)).build(story)


if __name__ == "__main__":
    build()
