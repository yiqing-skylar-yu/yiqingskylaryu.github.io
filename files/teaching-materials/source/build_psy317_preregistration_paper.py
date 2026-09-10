#!/usr/bin/env python3
"""Build the PSY 317 Preregistration Paper teaching-portfolio artifact."""

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
OUTPUT = HERE.parent / "PSY317_Preregistration_Paper_Assignment_and_Rubric.pdf"

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
        canvas.saveState(); canvas.setStrokeColor(colors.HexColor("#B8B8B8")); canvas.setLineWidth(.35)
        canvas.line(self.leftMargin, .43*inch, letter[0]-self.rightMargin, .43*inch)
        canvas.setFont("Georgia", 7.4); canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(self.leftMargin, .26*inch,
                          "PSY 317 Social Psychology Laboratory  \u00b7  Fall 2024  \u00b7  Yiqing \u201cSkylar\u201d Yu")
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
                             spaceBefore=7, spaceAfter=7, keepWithNext=True),
        "h2": ParagraphStyle("h2", fontName="Georgia-Bold", fontSize=11, leading=14,
                             spaceBefore=7, spaceAfter=4, keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Georgia", fontSize=9.15, leading=13, spaceAfter=7),
        "bullet": ParagraphStyle("bullet", fontName="Georgia", fontSize=9, leading=12.3,
                                 leftIndent=21, firstLineIndent=-10, bulletIndent=8, spaceAfter=4),
        "subbullet": ParagraphStyle("subbullet", fontName="Georgia", fontSize=8.75, leading=12,
                                    leftIndent=38, firstLineIndent=-10, bulletIndent=25, spaceAfter=3),
        "crit": ParagraphStyle("crit", fontName="Georgia-Bold", fontSize=9.1, leading=11.5),
        "desc": ParagraphStyle("desc", fontName="Georgia", fontSize=7.9, leading=10.4),
        "level": ParagraphStyle("level", fontName="Georgia-Bold", fontSize=7.9, leading=10.4),
        "pts": ParagraphStyle("pts", fontName="Georgia-Bold", fontSize=8, leading=10.4, alignment=TA_CENTER),
    }


RATING_5 = [("Great", "5 to >4.0"), ("Good", "4 to >3.0"), ("Fair", "3 to >2.0"), ("Need improvement", "2 to >0")]
RATING_10 = [("Great", "10 to >8.0"), ("Good", "8 to >6.0"), ("Fair", "6 to >4.0"), ("Need improvement", "4 to >0")]

CRITERIA = [
    {"name":"Description of the study's premises", "max":5,
     "description":"Describe the general premise of the study (e.g., what theory was being tested; what the research question was) and a summary of how they tested the theory/investigate the research question.", "levels":RATING_5},
    {"name":"Full details on preregistration and paper\u2019s hypotheses and whether they match", "max":10,
     "description":"You will closely examine 1) what the hypotheses were that were listed in the preregistration; 2) what the hypotheses were that are listed in the paper; 3) whether the hypotheses match; 4) whether there was anything in the article mentioned as a hypothesis that wasn\u2019t mentioned in the pre-registration (e.g., any new hypotheses added? Any omitted?).", "levels":RATING_10},
    {"name":"Full details on the variables listed in the preregistration and paper and whether they match", "max":10,
     "description":"You will also closely examine what the variables of interest were in the preregistration, and whether they are the same or different than what is in the paper. Were there any variables that come out of nowhere? Measured differently than intended? Lacking in detail on the preregistration?", "levels":RATING_10},
    {"name":"Full details on analyses, statistical tests, and sample size in the preregistration and paper and whether they match", "max":10,
     "description":"Look at what analyses/statistical tests were mentioned in the pre-registration, and whether they were mentioned in the paper and if they match. Also look at what the sample size was initially planned to be, and whether this matches what was collected in the paper. Consider other factors that may be different in the paper than in the preregistration.", "levels":RATING_10},
    {"name":"Full discussion about what was found", "max":25,
     "description":"Overall, how does your findings about the consistency between the published version and the pre-registration connect to what we have been learning so far? If you were to try and replicate the paper based on the preregistration alone, would you do differently? You need to demonstrate here what you have learned so far in the course about issues related to the replication crisis, replicability, QPRs and QMRs, p hacking, HARKing, power, validity/reliability, and anything else that is applicable to what you found.",
     "levels":[("Great","25 to >20.0"),("Good","20 to >15.0"),("Fair","15 to >10.0"),("Need improvement","10 to >0")]},
    {"name":"Writing is clear and concise", "max":5,
     "description":"Writing is exceptionally clear, concise, and easy to follow. No grammatical errors or awkward phrasing.", "levels":RATING_5},
    {"name":"Page length", "max":3,
     "description":"Meets page length requirements (6-8 pages, not including cover page and references).",
     "levels":[("Great","3 to >1.5"),("Fair","1.5 to >0.5"),("Need improvement","0.5 to >0")]},
    {"name":"APA title page", "max":1,
     "description":"Proper APA title page is included with all required elements (title, author's name, institutional affiliation, etc.).",
     "levels":[("Great","1 to >0.75"),("Minor issue","0.75 to >0.5"),("Need improvement","0.5 to >0.25"),("Missing","0.25 to >0")]},
    {"name":"APA text format", "max":2,
     "description":"Proper APA text formatting throughout the paper, including font, layout, and page numbers. Your paper needs to be in 12-point, consistent Font, double-spaced with 1-inch margins. Page numbers should be labeled on the top left corner.",
     "levels":[("Great","2 to >1.5"),("Minor issue","1.5 to >1.0"),("Need improvement","1 to >0.5"),("Missing","0.5 to >0")]},
    {"name":"APA references", "max":2,
     "description":"Proper APA references section and in-text citations throughout the paper.",
     "levels":[("Great","2 to >1.5"),("Minor issue","1.5 to >1.0"),("Need improvement","1 to >0.5"),("Missing","0.5 to >0")]},
]


def p(text, style):
    return Paragraph(escape(str(text)), style)


def criterion_block(c, s):
    unit = "point" if c["max"] == 1 else "points"
    rows = [[p(f"{c['name']} - {c['max']} {unit}", s["crit"]), p("", s["desc"]), p("Range", s["pts"])],
            [p("Criterion description", s["level"]), p(c["description"], s["desc"]), p("", s["pts"])]]
    for label, points in c["levels"]:
        rows.append([p(label, s["level"]), p("", s["desc"]), p(points, s["pts"])])
    table = Table(rows, colWidths=[1.35*inch, 4.50*inch, 1.0*inch], hAlign="LEFT")
    commands = [
        ("SPAN", (0,0), (1,0)), ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E5E5E5")),
        ("GRID", (0,0), (-1,-1), .4, colors.HexColor("#A8A8A8")),
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("ALIGN", (-1,0), (-1,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]
    commands.extend(("SPAN", (0,row), (1,row)) for row in range(2, len(rows)))
    table.setStyle(TableStyle(commands))
    return KeepTogether([table, Spacer(1, 9)])


def build():
    s=styles(); story=[
        Paragraph("Yiqing \u201cSkylar\u201d Yu", s["meta"]),
        Paragraph("PSY 317 Social Psychology Laboratory", s["meta"]),
        Paragraph("Fall 2024", s["meta"]), Spacer(1,7),
        Paragraph("Preregistration Paper", s["title"]),
        Paragraph("Assignment & Rubric", s["subtitle"]),
        Paragraph("<b>Portfolio context:</b> This midterm assignment asks students to compare a published social psychology study with its preregistration and evaluate their alignment. Students apply course concepts related to transparency, replicability, questionable research practices, statistical power, validity, and reliability.", s["context"]),
        Paragraph("Assignment Overview", s["h1"]),
        Paragraph("<b>Point value:</b> 73 points", s["body"]),
        Paragraph("For this assignment, read the instructions and write a paper using the rubric as your guide. Remember, this is a chance to show what you know. Do your best to incorporate course content into your responses.", s["body"]),
        Paragraph("Article Selection", s["h1"]),
    ]
    selection=[
        "Go to the Morgan Library main webpage and search for <i>Journal of Experimental Social Psychology</i>. Follow the journal\u2019s online-access link. When working off campus, use the library\u2019s proxy-server login to access articles.",
        "From the journal homepage on Elsevier ScienceDirect, browse recent issues or search for a paper that looks interesting and reports testing preregistered hypotheses. Evidence may appear in the abstract; searching the full text for \u201cOSF\u201d can also help locate preregistration information.",
        "Select one paper. If the paper reports multiple studies, choose one study that had a preregistration.",
        "Post the paper title and author list to the Canvas discussion forum by September 30 at 11:59 p.m. Do not choose a paper already selected by a classmate; the selection is guaranteed only after it is posted.",
    ]
    for i,x in enumerate(selection,1): story.append(Paragraph(f"{i}. {x}",s["bullet"]))
    story += [Paragraph("Paper Requirements",s["h1"]),
              Paragraph("Write a short paper examining how closely the authors\u2019 hypothesis testing followed what was preregistered. Use the Open Science Framework, or the site used by the authors, to locate the study preregistration.",s["body"])]
    requirements=[
        "Describe the general premise of the study, including the theory or research question, and summarize how the authors tested the theory or investigated the question.",
        "Compare the hypotheses in the preregistration with those in the published paper. Explain whether they match and identify any hypotheses added to or omitted from the article.",
        "Compare the variables of interest in the preregistration and paper. Identify variables that appear unexpectedly, were measured differently than intended, or lacked detail in the preregistration.",
        "Compare the planned and reported analyses or statistical tests. Compare the initially planned sample size with the sample collected and consider other differences between the paper and preregistration.",
        "Discuss what the consistency between the published paper and preregistration means in relation to course material. Explain what you would do differently if replicating the paper from the preregistration alone. Integrate relevant concepts such as the replication crisis, replicability, QPRs and QMRs, p hacking, HARKing, power, validity, and reliability.",
    ]
    for label,x in zip("abcde",requirements): story.append(Paragraph(f"{label}. {x}",s["bullet"]))
    story += [Paragraph("Formatting and Page Length",s["h1"])]
    formatting=[
        "Use 12-point Times New Roman, double spacing, and 1-inch margins. Place page numbers in the top-left corner.",
        "Use APA format, including a cover page, reference section, and APA-formatted in-text citations.",
        "Write 6-8 pages, excluding the cover page and references.",
        "Allocate approximately one-half to one page to the study premise, 3-4 pages to the study and preregistration descriptions and comparisons, and 2-3 pages to the discussion of findings and their consequences for the study\u2019s conclusions.",
        "See the APA student-paper setup guide: https://apastyle.apa.org/instructional-aids/student-paper-setup-guide.pdf",
    ]
    for x in formatting: story.append(Paragraph(x,s["bullet"],bulletText="\u2022"))
    story += [Paragraph("Collaboration and Academic Integrity",s["h1"]),
              Paragraph("This is an individual midterm paper. You may form small groups to review course materials together, but you must write the paper yourself.",s["body"])]
    integrity=[
        "Using AI for writing is prohibited in this course. Any signs of AI-generated text will lead to a report to the department for further review and a zero on this assignment.",
        "Do not copy and paste text directly from other sources, and avoid direct quotation.",
        "Cite every source you reference. Paraphrase source content rather than copying and pasting it.",
    ]
    for x in integrity: story.append(Paragraph(x,s["bullet"],bulletText="\u2022"))
    story += [Paragraph("Submission",s["h1"]),
              Paragraph("Submit the paper as a PDF in Canvas by October 9, 2024, at 11:59 p.m.",s["body"]),
              PageBreak(), Paragraph("Preregistration Paper Rubric",s["title"]),
              Paragraph("Total: 73 points",s["subtitle"])]
    for c in CRITERIA: story.append(criterion_block(c,s))
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); PortfolioDoc(str(OUTPUT)).build(story)


if __name__=="__main__": build()
