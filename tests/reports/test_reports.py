import json
import os

from app.services.reports import reports
from app.services.reports.models import (CreateCustomRequest,
                                         CreateDecisionsRequest,
                                         CreateReportRequest,
                                         CreateStatementsRequest,
                                         CreateTodosRequest, NoteInput)


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def test_todos_generic():
    data = load_json(os.path.join(os.path.dirname(__file__), "files", "todos.json"))
    transcripts = []
    for item in data["action_items"]:
        for note in item.get("notes", []):
            transcripts.append(note["excerpt"])

    notes = [
        NoteInput(
            note_id="test_note_1",
            transcripts=[{"text": transcript} for transcript in transcripts],
            metadata={"source": "test"},
        )
    ]

    req = CreateTodosRequest(
        notes=notes, language="English", llm_type="openai", model="o1"
    )
    response = reports.report_todos(req)
    assert hasattr(response, "title")
    assert hasattr(response, "action_items")
    assert isinstance(response.action_items, list)


def test_decisions_generic():
    data = load_json(os.path.join(os.path.dirname(__file__), "files", "decisions.json"))
    transcripts = []
    for decision in data["decisions"]:
        for note in decision.get("notes", []):
            transcripts.append(note["excerpt"])

    notes = [
        NoteInput(
            note_id="test_note_1",
            transcripts=[{"text": transcript} for transcript in transcripts],
            metadata={"source": "test"},
        )
    ]

    req = CreateDecisionsRequest(
        notes=notes, language="English", llm_type="openai", model="o1"
    )
    response = reports.report_decisions(req)
    assert hasattr(response, "title")
    assert hasattr(response, "decisions")
    assert isinstance(response.decisions, list)


def test_statements_generic():
    data = load_json(
        os.path.join(os.path.dirname(__file__), "files", "statements.json")
    )
    transcripts = [item["statement"] for item in data["statements"]]

    notes = [
        NoteInput(
            note_id="test_note_1",
            transcripts=[{"text": transcript} for transcript in transcripts],
            metadata={"source": "test"},
        )
    ]

    req = CreateStatementsRequest(
        notes=notes, language="English", llm_type="openai", model="o1"
    )
    response = reports.report_statements(req)
    assert hasattr(response, "title")
    assert hasattr(response, "statements")
    assert isinstance(response.statements, list)


def test_summary_generic():
    data = load_json(os.path.join(os.path.dirname(__file__), "files", "summary.json"))
    transcripts = []
    for theme in data["report"]["themes"]:
        for note in theme["notes"]:
            transcripts.append(note["excerpt"])

    notes = [
        NoteInput(
            note_id="test_note_1",
            transcripts=[{"text": transcript} for transcript in transcripts],
            metadata={"source": "test"},
        )
    ]

    req = CreateReportRequest(
        notes=notes, language="English", llm_type="openai", model="o1"
    )
    response = reports.report_summary(req)
    assert hasattr(response, "report")
    assert response.report is not None
    assert hasattr(response.report, "overall_topic")
    assert hasattr(response.report, "themes")
    assert isinstance(response.report.themes, list)


def test_custom_report_generic():
    transcripts = [
        "The team decided to launch the new product next quarter.",
        "John will prepare the marketing plan. The deadline is August 1st.",
        "We need to assess funding for the new campaign effectively.",
        "The initial campaign design is complete and ready for review.",
        "Stakeholder approval is required by next week.",
        "Lisa recommended increasing investment in digital marketing.",
        "We need to review campaign progress and budget allocation.",
        "Mike volunteered to schedule the review meeting with stakeholders for Friday.",
        "The meeting topic is Campaign Review and Budget Planning.",
        "Meeting records indicate the date of July 8th, 2024.",
        "Stakeholder approval is needed before finalizing campaign activities.",
        "The campaign design is ready for review.",
        "Stakeholder approval is needed by next week.",
        "Budget considerations emerged as a shared priority.",
    ]

    notes = [
        NoteInput(
            note_id="test_note_1",
            transcripts=[{"text": transcript} for transcript in transcripts],
            metadata={"source": "test"},
        )
    ]

    req = CreateCustomRequest(
        notes=notes,
        language="English",
        llm_type="openai",
        model="o1",
        custom_prompt="Create a comprehensive report with sections and bullet points based on the meeting transcripts.",
    )
    response = reports.report_custom(req)
    assert hasattr(response, "data")
    assert response.data is not None
    assert hasattr(response.data, "title")
    assert hasattr(response.data, "summary")
    assert hasattr(response.data, "sections")
    assert isinstance(response.data.sections, list)
    if len(response.data.sections) > 0:
        assert hasattr(response.data.sections[0], "heading")
        assert hasattr(response.data.sections[0], "bullet_points")
        assert isinstance(response.data.sections[0].bullet_points, list)
