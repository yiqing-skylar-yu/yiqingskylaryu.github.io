#!/usr/bin/env python3
"""Build the PSY 250 Final Research Proposal teaching-portfolio artifact."""

from pathlib import Path
from html import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "PSY250_Final_Research_Proposal_Assignment_and_Rubric.pdf"

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
        canvas.setStrokeColor(colors.HexColor("#B8B8B8")); canvas.setLineWidth(.35)
        canvas.line(self.leftMargin, .43*inch, letter[0]-self.rightMargin, .43*inch)
        canvas.setFont("Georgia", 7.4); canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(self.leftMargin, .26*inch,
                          "PSY 250 Research Design & Analysis I  \u00b7  Summer 2026  \u00b7  Yiqing \u201cSkylar\u201d Yu")
        canvas.drawRightString(letter[0]-self.rightMargin, .26*inch, f"Page {doc.page}")
        canvas.restoreState()


def styles():
    return {
        "meta": ParagraphStyle("meta", fontName="Georgia", fontSize=9, leading=12,
                               alignment=TA_CENTER, textColor=colors.HexColor("#3F3F3F"), spaceAfter=2),
        "title": ParagraphStyle("title", fontName="Georgia-Bold", fontSize=21, leading=24,
                                alignment=TA_CENTER, spaceAfter=2),
        "subtitle": ParagraphStyle("subtitle", fontName="Georgia", fontSize=13, leading=16,
                                   alignment=TA_CENTER, spaceAfter=14),
        "context": ParagraphStyle("context", fontName="Georgia-Italic", fontSize=8.6, leading=12,
                                  leftIndent=8, rightIndent=8, spaceAfter=14),
        "h1": ParagraphStyle("h1", fontName="Georgia-Bold", fontSize=14, leading=17,
                             spaceBefore=6, spaceAfter=7, keepWithNext=True),
        "h2": ParagraphStyle("h2", fontName="Georgia-Bold", fontSize=11, leading=14,
                             spaceBefore=7, spaceAfter=4, keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Georgia", fontSize=9.2, leading=13, spaceAfter=7),
        "bullet": ParagraphStyle("bullet", fontName="Georgia", fontSize=9.1, leading=12.5,
                                 leftIndent=21, firstLineIndent=-10, bulletIndent=8, spaceAfter=4),
        "subbullet": ParagraphStyle("subbullet", fontName="Georgia", fontSize=8.8, leading=12,
                                    leftIndent=38, firstLineIndent=-10, bulletIndent=25, spaceAfter=3),
        "crit": ParagraphStyle("crit", fontName="Georgia-Bold", fontSize=9.1, leading=11.5),
        "desc": ParagraphStyle("desc", fontName="Georgia", fontSize=7.8, leading=10.3),
        "level": ParagraphStyle("level", fontName="Georgia-Bold", fontSize=7.8, leading=10.3),
        "pts": ParagraphStyle("pts", fontName="Georgia-Bold", fontSize=8, leading=10.3, alignment=TA_CENTER),
        "small": ParagraphStyle("small", fontName="Georgia", fontSize=8.3, leading=11.2),
    }


CRITERIA = [
    {
        "name": "Title Page", "max": 4, "description": "",
        "levels": [("Full Marks", 4, "Contains all components"),
                   ("Partial Marks", 2, "Missing some components"),
                   ("No Marks", 0, "Missing many components or missing entirely")],
    },
    {
        "name": "Statement of the Importance of the Problem.", "max": 4,
        "description": "What is the research problem & why is this research important to do? Possible implications. This is usually related to the DV. This should be supported by at least 1 source.",
        "levels": [("Full Marks", 4, "Clear and supported argument and identification of real-world issue."),
                   ("Partial Marks", 3, "Identified a problem but importance is weakly identified, typically no support or gaps in reasoning."),
                   ("Partial Marks", 2, "Identified problem but it is stating the hypothesis instead of a real-world issue"),
                   ("No Marks", 0, "Weak identification of research problem and little or no argument for importance.")],
    },
    {
        "name": "Well-developed Introduction.", "max": 18,
        "description": "Used relevant scientific sources to build up to and support the hypothesis, methodology and choice of participants.",
        "levels": [("Full Marks", 18, "Provides strong supporting evidence of previous research and connects logically to current study. Reader can predict hypothesis by the end of the paper before being stated."),
                   ("Partial Marks", 17, "Provides strong evidence but weak connection to current study."),
                   ("Parital Marks", 15, "Related studies but provide weak evidence that does not connect to hypothesis and methodology."),
                   ("Partial Marks", 15, "Provides weak supporting evidence that may not connect to hypothesis OR Inappropriate choice of methodology."),
                   ("Partial Marks", 11, "Peripherally related studies that offer no support to current study."),
                   ("Partial Marks", 9, "Most research presented is not related to current study."),
                   ("No Marks", 0, "Very little research is presented and research presented is not related to current study.")],
    },
    {
        "name": "Testable Hypothesis", "max": 4,
        "description": "Clearly stated testable directional hypothesis that involves at least one independent variable and one dependent variable.",
        "levels": [("Full Marks", 4, "Clearly stated testable directional hypothesis with at least one IV & one DV."),
                   ("Partial Marks", 3, "Unclear or awkward or nondirectional testable hypothesis with at least one IV & one DV."),
                   ("Partial Marks", 2, "Hypothesis is testable but IV or DV not clear."),
                   ("No Marks", 0, "Untestable hypothesis.")],
    },
    {
        "name": "Appropriate Participants", "max": 4,
        "description": "Clearly Identify and describe the participants, sample size, sampling method, compensation.",
        "levels": [("Full Marks", 4, "Participants are appropriate for stated hypothesis. Participants\u2019 relevant demographic characteristics are identified (e.g., age, gender, ethnicity and any other relevant to study). Sample size is identified and sampling/recruiting methods identified and compensation."),
                   ("No Marks", 0, "1 point will be deducted for each missing requirement.")],
    },
    {
        "name": "Dependent Variable", "max": 6,
        "description": "Selected an appropriate DV to test hypothesis. Clearly describes how DV(s) would be measured. Specific Information about DVs(e.g., surveys, tests, and observational methods).",
        "levels": [("Full Marks", 6, "Appropriate DV described in enough detail to allow for replication."),
                   ("Partial Marks", 5, "Appropriate DV described with detail but not enough to allow for replication."),
                   ("Partial Marks", 4, "Appropriate DV described but 2 or more critical elements are missing making it unclear (e.g., stimuli being presented or number of items on a test)."),
                   ("Partial Marks", 3, "Appropriate DV but description is vague with multiple missing elements."),
                   ("No Marks", 0, "Appropriate DV but measure is unclear and inadequate OR Inappropriate DV.")],
    },
    {
        "name": "Procedures", "max": 6,
        "description": "Clear and well-designed research design. The steps must be clearly identified. The IV(s) are clearly identified AND described. The procedure is adequate for the hypothesis (levels of IV should match the hypothesis).",
        "levels": [("Full Marks", 6, "Appropriate procedures to test hypothesis with at least 2 levels of IV. Clear step-by- step description of procedures, enough detail to allow for replication."),
                   ("Partial Marks", 5, "Appropriate procedures to test hypothesis with at least 2 levels of IV. Clear step-by- step description of procedures but not enough detail to allow for replication."),
                   ("Partial Marks", 4, "Appropriate procedures to test hypothesis with at least 2 levels of IV. Provides some description of procedures but lack minor details or are confusing in some areas."),
                   ("Partial Marks", 3, "Provide some description of procedures but lack multiple details OR Procedures to test hypothesis may be somewhat inappropriate (major logical flaws or limitations)."),
                   ("No Marks", 0, "Description of procedures is disorganized, incomprehensible, and/or lack substantial details OR Procedures to test hypothesis do not appear appropriate")],
    },
    {
        "name": "Ethical Information", "max": 2, "description": "",
        "levels": [("Full Marks", 2, "Includes all relevant ethical information- consent- debriefing etc."),
                   ("Partial Marks", 1, "Missing some information"),
                   ("No Marks", 0, "Missing a lot of information or missing entirely")],
    },
    {
        "name": "Sources", "max": 5,
        "description": "Utilized Springboard article and four other primary sources.",
        "levels": [("Full Marks", 5, "Relevant citation for springboard article and reviews four other primary sources."),
                   ("No Marks", 0, "Lose 1 point for each missing source.")],
    },
    {
        "name": "Spelling, Grammar, Clarity", "max": 7,
        "description": "Well written, edited paper. Paper should have good flow and transitions. Paper length is typically 4-6 pages. 1 free grammar or spelling mistake will be allowed per page of text (not title or reference page).",
        "levels": [("Full Marks", 7, "Good flow, nice transitions, information is clearly presented, and no more than 1 mistake per page."),
                   ("Partial Marks", 6, "Mostly good flow, transitions, and most information is clearly presented. Noticeable improvements in style could be made, but no more than 1 mistake per page."),
                   ("Partial Marks", 4, "Poor flow, transitions, and information is not clearly presented, but no more than 1 mistake per page"),
                   ("No Marks", 0, "Lose 1 point for each additional grammar or spelling error.")],
    },
    {
        "name": "APA Style", "max": 20,
        "description": "APA style is correct for title page, text of Paper and Reference page",
        "levels": [("Full Marks", 20, "Lose \u00bd point for each error. If make the same mistake consistently that was identified in the introduction you will lose \u00bd point for each time."),
                   ("No Marks", 0, "")],
    },
    {
        "name": "Extra Credit", "max": 0,
        "description": "Identify at least 1 Potential Confounding variable",
        "levels": [("Full Marks", 0, "Earn up to 2 points"), ("No Marks", 0, "")],
    },
    {
        "name": "Deductions", "max": 0, "description": "",
        "levels": [("Design", 0, "If design is not an experiment, you will lose 20 points."),
                   ("Intorduction", 0, "If you did NOT remove Brief Introduction to Methods from introduction, you will lose 2 points."),
                   ("Springboard", 0, "If your proposals does Not have relevant connection to springboard, you will lose 5 points.")],
    },
]


def p(text, style):
    return Paragraph(escape(str(text)), style)


def criterion_block(c, s):
    title = f"{c['name']} - {c['max']} points"
    rows = [[p(title, s["crit"]), p("", s["desc"]), p("Points", s["pts"])]]
    if c["description"]:
        rows.append([p("Criterion description", s["level"]), p(c["description"], s["desc"]), p("", s["pts"])])
    for label, pts, desc in c["levels"]:
        rows.append([p(label, s["level"]), p(desc, s["desc"]), p(pts, s["pts"])])
    table = Table(rows, colWidths=[1.28*inch, 4.92*inch, .65*inch], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("SPAN", (0,0), (1,0)),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E5E5E5")),
        ("GRID", (0,0), (-1,-1), .4, colors.HexColor("#A8A8A8")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (-1,0), (-1,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    return KeepTogether([table, Spacer(1, 9)])


def build():
    s = styles()
    story = [
        Paragraph("Yiqing \u201cSkylar\u201d Yu", s["meta"]),
        Paragraph("PSY 250 Research Design & Analysis I", s["meta"]),
        Paragraph("Summer 2026", s["meta"]), Spacer(1, 7),
        Paragraph("Final Research Proposal", s["title"]),
        Paragraph("Assignment & Rubric", s["subtitle"]),
        Paragraph("<b>Portfolio context:</b> This culminating assignment brings together the scaffolded research-design and writing activities completed throughout the course. Students revise earlier components using instructor feedback and integrate them into a complete APA-style research proposal.", s["context"]),
        Paragraph("Assignment Overview", s["h1"]),
        Paragraph("<b>Point value:</b> 80 points", s["body"]),
        Paragraph("This assignment brings together all the work you have completed so far into a final research proposal.", s["body"]),
        Paragraph("Supporting Course Resources", s["h2"]),
    ]
    for resource in ["Lecture: Final Research Proposal", "Lecture: APA In-Text Citation",
                     "Lecture: APA References & Citations", "Lecture: APA Style/Writing Guidelines"]:
        story.append(Paragraph(resource, s["bullet"], bulletText="\u2022"))
    story += [Paragraph("Instructions", s["h1"]),
              Paragraph("Students were provided with two example research proposals in Canvas.", s["bullet"], bulletText="\u2022"),
              Paragraph("Revise your Introduction based on feedback from the Introduction Assignment. Use the feedback you received to strengthen your introduction.", s["bullet"], bulletText="\u2022"),
              Paragraph("Expand your Method Outline to complete the full proposal based on the feedback.", s["bullet"], bulletText="\u2022"),
              Paragraph("Method Section", s["h1"]),
              Paragraph("Your Method section should provide enough detail for another researcher to replicate your study. Follow APA format and consult your APA manual for structure and style.", s["body"]),
              Paragraph("Minimum sections (you may include more)", s["h2"]),
              Paragraph("Participants", s["h2"])]
    for item in [
        "Who will participate in the study?",
        "How many participants? Aim for at least 40 per group, using similar studies as a guide.",
        "What sampling method will you use?",
        "How will you recruit them (e.g., flyers, online ads, community outreach)?",
        "What are the expected participant characteristics (e.g., age, gender, ethnicity)?",
        "Are there eligibility criteria (e.g., clinical diagnosis, experience level)?",
        "What will motivate participation? Specify compensation (e.g., course credit, gift card, treatment).",
    ]:
        story.append(Paragraph(item, s["subbullet"], bulletText="\u2022"))
    story.append(Paragraph("Materials", s["h2"]))
    for item in [
        "Describe all materials used to measure or manipulate your variables. Explain your choices and provide citations.",
        "Ensure you address every variable in your hypotheses. Do not include unrelated measures.",
        "You do not need to provide full surveys or stimuli, but describe them in enough detail for the reader to visualize.",
        "Include any equipment, surveys, drugs, or stimuli used.",
    ]:
        story.append(Paragraph(item, s["subbullet"], bulletText="\u2022"))
    story.append(Paragraph("Procedure", s["h2"]))
    for item in [
        "Specify your design (within-subjects or between-subjects).",
        "Detail each step of the participant experience from start to finish.",
        "Indicate study location (lab, field, online), duration, and participant instructions.",
        "Outline the study timeline, including the number of data collection points.",
        "Clarify incentives provided to participants.",
        "Address any ethical considerations, including consent and debriefing.",
    ]:
        story.append(Paragraph(item, s["subbullet"], bulletText="\u2022"))
    story += [Paragraph("Formatting Reminders", s["h1"])]
    for item in [
        "Write in future tense (this is a proposal).",
        "Use active voice.",
        "Justify your design choices and explain how they support your hypotheses.",
        "Use appropriate terminology to demonstrate mastery of course material.",
    ]:
        story.append(Paragraph(item, s["bullet"], bulletText="\u2022"))
    story += [Paragraph("Finalize and Format Your Proposal", s["h1"]),
              Paragraph("When you\u2019ve completed your Method section and revised your Introduction, carefully review APA guidelines to ensure proper formatting.", s["body"]),
              Paragraph("Your final paper must include:", s["body"])]
    for item in [
        "An APA-style title page",
        "A fully written and edited introduction",
        "A fully written method section",
        "A reference page with at least five primary sources (one must be your springboard article)",
    ]:
        story.append(Paragraph(item, s["bullet"], bulletText="\u2022"))
    story += [Paragraph("Optional: tables or figures (APA-compliant) and extra credit.", s["body"]),
              Paragraph("Be sure your final paper follows the guidelines and expectations outlined in the description and rubric.", s["body"]),
              PageBreak(),
              Paragraph("Final Proposal Rubric", s["title"]),
              Paragraph("Total: 80 points", s["subtitle"])]
    for c in CRITERIA:
        story.append(criterion_block(c, s))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PortfolioDoc(str(OUTPUT)).build(story)


if __name__ == "__main__":
    build()
