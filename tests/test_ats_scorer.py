import pytest
from src.ats_scorer import ATSScorer


SAMPLE_RESUME = """
John Doe
john.doe@example.com
(555) 123-4567
New York, NY

SUMMARY
Experienced software developer with 5 years of experience building scalable systems.

EXPERIENCE
Senior Developer at Tech Corp 2019-2024
- Led development of microservices architecture
- Implemented CI/CD pipelines that improved deployment frequency by 40%
- Managed team of 5 engineers and delivered 3 major product launches

EDUCATION
B.S. Computer Science, State University 2019

SKILLS
Python, JavaScript, React, AWS, Docker, PostgreSQL
"""


@pytest.fixture
def scorer():
    return ATSScorer()


def test_calculate_score_returns_required_keys(scorer):
    result = scorer.calculate_score(SAMPLE_RESUME)
    assert "overall_score" in result
    assert "category_scores" in result
    assert "feedback" in result
    assert "grade" in result


def test_overall_score_in_valid_range(scorer):
    result = scorer.calculate_score(SAMPLE_RESUME)
    assert 0 <= result["overall_score"] <= 100


def test_category_scores_present(scorer):
    result = scorer.calculate_score(SAMPLE_RESUME)
    expected = {"format", "sections", "keywords", "content", "contact"}
    assert expected == set(result["category_scores"].keys())


def test_grade_a_plus(scorer):
    assert scorer._get_grade(95) == "A+"


def test_grade_a(scorer):
    assert scorer._get_grade(85) == "A"


def test_grade_b(scorer):
    assert scorer._get_grade(75) == "B"


def test_grade_c(scorer):
    assert scorer._get_grade(65) == "C"


def test_grade_d(scorer):
    assert scorer._get_grade(50) == "D"


def test_calculate_score_with_job_description(scorer):
    jd = "Looking for a Python developer with AWS and Docker experience."
    result = scorer.calculate_score(SAMPLE_RESUME, job_description=jd)
    assert result["overall_score"] > 0


def test_contact_score_detects_email(scorer):
    result = scorer._calculate_contact_score("Contact: john@example.com")
    assert result["score"] >= 40
    assert "email" in result["found_contact"]


def test_contact_score_detects_phone(scorer):
    result = scorer._calculate_contact_score("Phone: (555) 123-4567")
    assert result["score"] >= 30
    assert "phone" in result["found_contact"]


def test_contact_score_empty_text(scorer):
    result = scorer._calculate_contact_score("No contact details here")
    assert result["score"] == 0
    assert result["found_contact"] == []


def test_format_score_clean_text(scorer):
    result = scorer._calculate_format_score("Clean text without special chars.")
    assert result["score"] > 70


def test_content_score_short_resume(scorer):
    result = scorer._calculate_content_score("Too short.")
    assert result["score"] < 70


def test_feedback_is_list(scorer):
    result = scorer.calculate_score(SAMPLE_RESUME)
    assert isinstance(result["feedback"], list)
    assert len(result["feedback"]) > 0
