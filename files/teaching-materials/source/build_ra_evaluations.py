#!/usr/bin/env python3
"""Build the public, anonymized research-assistant mentoring evaluation record."""

from collections import OrderedDict
from html import escape
from pathlib import Path
import argparse

from openpyxl import load_workbook
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


TERM_CONTEXT = OrderedDict([
    ("Spring 2022", ("Postbaccalaureate", 5, 2)),
    ("Fall 2022", ("PhD program; midsemester evaluation", 9, 6)),
    ("Spring 2023", ("PhD program", 12, 8)),
    ("Fall 2023", ("PhD program", 8, 7)),
    ("Spring 2024", ("PhD program", 12, 10)),
    ("Fall 2024", ("PhD program", 14, 10)),
    ("Spring 2025", ("PhD program", 18, 11)),
    ("Spring 2026", ("PhD program", 16, 7)),
    ("Summer 2026", ("PhD program", 10, 6)),
])


def text(value):
    return "" if value is None else str(value)


def ptext(value):
    return escape(text(value)).replace("\n", "<br/>")


def percent(value):
    return f"{100 * value:.1f}%"


class MentoringEvaluationDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=letter,
            leftMargin=0.55 * inch,
            rightMargin=0.55 * inch,
            topMargin=0.58 * inch,
            bottomMargin=0.55 * inch,
            title="Research Assistant Mentoring Evaluations",
            author="Yiqing Skylar Yu",
            subject="Anonymized research-assistant evaluations for an academic teaching portfolio",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates(PageTemplate(id="all", frames=frame, onPage=self.header_footer))

    def header_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#B9B9B9"))
        canvas.setLineWidth(0.35)
        if doc.page > 1:
            canvas.line(self.leftMargin, letter[1] - 0.39 * inch,
                        letter[0] - self.rightMargin, letter[1] - 0.39 * inch)
            canvas.setFont("Georgia", 7.4)
            canvas.setFillColor(colors.HexColor("#555555"))
            canvas.drawString(self.leftMargin, letter[1] - 0.31 * inch,
                              "Yiqing \u201cSkylar\u201d Yu  |  Research Assistant Mentoring Evaluations")
        canvas.line(self.leftMargin, 0.38 * inch,
                    letter[0] - self.rightMargin, 0.38 * inch)
        canvas.setFont("Georgia", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawRightString(letter[0] - self.rightMargin, 0.22 * inch, f"Page {doc.page}")
        canvas.restoreState()


def make_styles():
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow", fontName="Georgia", fontSize=8, leading=10,
            textColor=colors.HexColor("#444444"), alignment=TA_CENTER, spaceAfter=3,
        ),
        "title": ParagraphStyle(
            "title", fontName="Georgia-Bold", fontSize=20, leading=23,
            alignment=TA_CENTER, textColor=colors.HexColor("#161616"), spaceAfter=5,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", fontName="Georgia", fontSize=12.5, leading=15,
            alignment=TA_CENTER, spaceAfter=12,
        ),
        "h1": ParagraphStyle(
            "h1", fontName="Georgia-Bold", fontSize=14, leading=17,
            spaceBefore=9, spaceAfter=6, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="Georgia-Bold", fontSize=10.8, leading=13,
            spaceBefore=8, spaceAfter=4, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "h3", fontName="Georgia-Bold", fontSize=9, leading=11.2,
            spaceBefore=7, spaceAfter=3, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body", fontName="Georgia", fontSize=8.35, leading=11.2, spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "small", fontName="Georgia", fontSize=7.15, leading=8.7,
        ),
        "smallb": ParagraphStyle(
            "smallb", fontName="Georgia-Bold", fontSize=7.15, leading=8.7,
        ),
        "comment": ParagraphStyle(
            "comment", fontName="ArialUnicode", fontSize=7.75, leading=10.2,
            leftIndent=10, rightIndent=3, spaceAfter=5,
        ),
        "record": ParagraphStyle(
            "record", fontName="Georgia", fontSize=7.2, leading=9.2,
            textColor=colors.HexColor("#444444"),
        ),
    }


def academic_table(data, widths, styles, aligns=None, repeat_rows=1, compact=False):
    rows = []
    for row_index, row in enumerate(data):
        style = styles["smallb"] if row_index == 0 else styles["small"]
        rows.append([Paragraph(ptext(value), style) for value in row])
    padding = 3 if compact else 4
    table = Table(rows, colWidths=widths, repeatRows=repeat_rows, hAlign="LEFT", splitByRow=1)
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), padding),
        ("RIGHTPADDING", (0, 0), (-1, -1), padding),
        ("TOPPADDING", (0, 0), (-1, -1), padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8B8B8")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111111")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F8F8")]),
    ]
    if aligns:
        for column, alignment in enumerate(aligns):
            commands.append(("ALIGN", (column, 1), (column, -1), alignment))
    table.setStyle(TableStyle(commands))
    return table


def read_workbook(path):
    workbook = load_workbook(path, data_only=True, read_only=True)
    summary = list(workbook["Summary"].iter_rows(min_row=16, max_row=22, min_col=1, max_col=5, values_only=True))
    trends = list(workbook["Term trends"].iter_rows(min_row=5, min_col=1, max_col=10, values_only=True))
    activities = list(workbook["Activity ratings"].iter_rows(min_row=5, min_col=1, max_col=6, values_only=True))
    responses = list(workbook["Written responses"].iter_rows(min_row=5, min_col=1, max_col=5, values_only=True))
    return summary, trends, activities, responses


def add_title(story, styles):
    story.extend([
        Paragraph("Yiqing \u201cSkylar\u201d Yu", styles["eyebrow"]),
        Paragraph("Colorado State University", styles["eyebrow"]),
        Spacer(1, 3),
        Paragraph("Research Assistant Mentoring Evaluations", styles["title"]),
        Paragraph("Spring 2022 - Summer 2026", styles["subtitle"]),
    ])


def add_overview(story, styles, summary):
    story.append(Paragraph("Evaluation overview", styles["h1"]))
    overview = [["Evaluation period", "Career stage", "RAs mentored", "Evaluations", "Approx. coverage"]]
    total_mentored = total_completed = 0
    for term, (stage, mentored, completed) in TERM_CONTEXT.items():
        overview.append([term, stage, mentored, completed, percent(completed / mentored)])
        total_mentored += mentored
        total_completed += completed
    overview.append(["Total", "", total_mentored, total_completed, percent(total_completed / total_mentored)])
    story.append(academic_table(
        overview, [78, 156, 72, 64, 78], styles,
        aligns=["LEFT", "LEFT", "CENTER", "CENTER", "CENTER"], compact=True,
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Coverage is approximate because semester headcounts and survey eligibility may not correspond perfectly. "
        "Spring 2022 reflects mentoring completed as a postbaccalaureate researcher; the PhD program began in Fall 2022.",
        styles["record"],
    ))

    story.append(Paragraph("Comparable ratings across evaluation periods", styles["h2"]))
    ratings = [["Mentoring measure", "N", "Mean", "Favorable (4-5)"]]
    for metric, n, mean_value, favorable, _scope in summary:
        ratings.append([metric, n, f"{mean_value:.2f}", percent(favorable)])
    story.append(academic_table(
        ratings, [262, 46, 60, 100], styles,
        aligns=["LEFT", "CENTER", "CENTER", "CENTER"], compact=True,
    ))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Across 67 completed evaluations, research assistants consistently rated the mentoring relationship and research experience positively. "
        "Written feedback emphasizes clear and supportive guidance, practical research learning, increased confidence, and professional development. "
        "Recurring suggestions include more exposure to data analysis, refresher training, early team-building, and clearer expectations for quality checks and independent project work.",
        styles["body"],
    ))


def add_term(story, styles, term, trend, activities, responses):
    story.append(PageBreak())
    stage, mentored, completed = TERM_CONTEXT[term]
    story.append(Paragraph(term, styles["h1"]))
    story.append(Paragraph(
        f"{stage}. Research assistants mentored: {mentored}. Completed evaluations: {completed} "
        f"({percent(completed / mentored)} approximate coverage).",
        styles["body"],
    ))

    metric_names = [
        "Mentor knowledgeable",
        "Mentor enthusiastic",
        "Mentor prepared",
        "Experiment-session instructions clear",
        "Overall mentor rating",
        "Overall research experience",
        "Experience met expectations",
    ]
    metric_values = trend[3:10]
    available_metrics = [[name, f"{value:.2f}"] for name, value in zip(metric_names, metric_values) if value is not None]
    if available_metrics:
        story.append(Paragraph("Comparable 1-5 ratings", styles["h2"]))
        story.append(Paragraph(
            "Means are shown for items included in this period's instrument. Blank or omitted items were not collected.",
            styles["record"],
        ))
        story.append(Spacer(1, 3))
        story.append(academic_table(
            [["Evaluation item", "Mean"]] + available_metrics,
            [410, 58], styles, aligns=["LEFT", "CENTER"], compact=True,
        ))

    term_activities = [row for row in activities if row[0] == term]
    if term_activities:
        scales = sorted({text(row[5]) for row in term_activities})
        story.append(Paragraph("Activity ratings", styles["h2"]))
        story.append(Paragraph(
            "Scale: " + "; ".join(scales) + ". Response counts vary when respondents did not participate or selected not applicable.",
            styles["record"],
        ))
        story.append(Spacer(1, 3))
        activity_data = [["Activity", "N", "Mean", "Scale"]]
        for _term, _stage, activity, n, mean_value, scale in term_activities:
            activity_data.append([activity, n, f"{mean_value:.2f}", scale])
        story.append(academic_table(
            activity_data, [324, 42, 52, 82], styles,
            aligns=["LEFT", "CENTER", "CENTER", "CENTER"], compact=True,
        ))

    term_responses = [row for row in responses if row[0] == term]
    if term_responses:
        story.append(Paragraph("Anonymous written responses", styles["h2"]))
        grouped = OrderedDict()
        for _term, _stage, response_id, question, answer in term_responses:
            grouped.setdefault(question, []).append((response_id, answer))
        for question, answers in grouped.items():
            story.append(Paragraph(ptext(question), styles["h3"]))
            for response_id, answer in answers:
                story.append(Paragraph(
                    f'<font name="Georgia-Bold">{ptext(response_id)}.</font> {ptext(answer)}',
                    styles["comment"],
                ))


def build(input_path, output_path):
    summary, trends, activities, responses = read_workbook(input_path)
    trend_by_term = {row[0]: row for row in trends if row[0] in TERM_CONTEXT}
    missing = [term for term in TERM_CONTEXT if term not in trend_by_term]
    if missing:
        raise ValueError(f"Missing term trend rows: {missing}")

    styles = make_styles()
    story = []
    add_title(story, styles)
    add_overview(story, styles, summary)
    for term in TERM_CONTEXT:
        add_term(story, styles, term, trend_by_term[term], activities, responses)
    story.extend([
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#999999")),
        Spacer(1, 5),
        Paragraph("Evaluation record", styles["h3"]),
        Paragraph(
            "This document contains the complete anonymized quantitative summaries and written responses currently compiled for the nine evaluation periods listed above. "
            "Names, IP addresses, response IDs, email fields, timestamps, and other administrative metadata are excluded.",
            styles["record"],
        ),
    ])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    MentoringEvaluationDoc(str(output_path)).build(story)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    pdfmetrics.registerFont(TTFont("Georgia", "/System/Library/Fonts/Supplemental/Georgia.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"))
    pdfmetrics.registerFont(TTFont("ArialUnicode", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"))
    build(args.input, args.output)


if __name__ == "__main__":
    main()
