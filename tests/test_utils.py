import json
import os
import pytest
from src.utils import (
    format_skills_list,
    truncate_text,
    create_result_summary,
    get_timestamp,
    validate_file_upload,
)


def test_format_skills_list():
    skills = {"programming": ["Python", "Java"], "web": ["React"]}
    result = format_skills_list(skills)
    assert "Programming" in result
    assert "Python" in result
    assert "React" in result


def test_format_skills_list_empty():
    assert format_skills_list({}) == ""


def test_truncate_text_short():
    text = "Short text"
    assert truncate_text(text, 100) == text


def test_truncate_text_long():
    text = "A" * 200
    result = truncate_text(text, 100)
    assert len(result) == 100
    assert result.endswith("...")


def test_truncate_text_exact():
    text = "A" * 100
    assert truncate_text(text, 100) == text


def test_create_result_summary_with_ats():
    results = {"ats_score": {"overall_score": 75, "grade": "B"}}
    summary = create_result_summary(results)
    assert "75" in summary
    assert "B" in summary


def test_create_result_summary_with_skills():
    results = {"skills": {"programming": ["Python", "Java"], "web": ["React"]}}
    summary = create_result_summary(results)
    assert "3" in summary


def test_create_result_summary_empty():
    assert create_result_summary({}) == ""


def test_get_timestamp():
    ts = get_timestamp()
    assert len(ts) > 0
    assert "-" in ts


def test_validate_file_upload_missing():
    with pytest.raises(FileNotFoundError):
        validate_file_upload("/nonexistent/file.pdf")


def test_validate_file_upload_valid_txt(tmp_path):
    f = tmp_path / "resume.txt"
    f.write_text("sample resume content")
    assert validate_file_upload(str(f)) is True


def test_validate_file_upload_invalid_extension(tmp_path):
    f = tmp_path / "resume.xlsx"
    f.write_text("some content")
    with pytest.raises(ValueError, match="Invalid file type"):
        validate_file_upload(str(f))


def test_validate_file_upload_too_large(tmp_path):
    f = tmp_path / "big.pdf"
    f.write_bytes(b"x" * (11 * 1024 * 1024))  # 11 MB
    with pytest.raises(ValueError, match="File too large"):
        validate_file_upload(str(f))
