import pytest
from services import extract_text, make_quiz, make_study_plan, analyze_weak_topics

class Upload:
    name = "notes.txt"
    def __init__(self, data=b"Photosynthesis converts light energy into chemical energy."):
        self.data = data
    def getvalue(self): return self.data

def test_extract_text():
    assert "Photosynthesis" in extract_text(Upload())

def test_extract_rejects_unsupported_type():
    u=Upload(); u.name="notes.exe"
    with pytest.raises(ValueError): extract_text(u)

def test_extract_rejects_oversized_file():
    with pytest.raises(ValueError): extract_text(Upload(b"x" * (10*1024*1024+1)))

def test_quiz_is_explicit_demo_without_aws(monkeypatch):
    monkeypatch.delenv("AWS_REGION",raising=False); monkeypatch.delenv("AWS_DEFAULT_REGION",raising=False)
    q=make_quiz("Biology","","Easy",4)
    assert len(q["questions"])==4 and q["demo"] is True
    assert all(x["answer"] in x["options"] for x in q["questions"])

def test_quiz_validates_count(monkeypatch):
    monkeypatch.delenv("AWS_REGION",raising=False)
    with pytest.raises(ValueError): make_quiz("Biology","","Easy",0)

def test_plan_has_real_newlines(monkeypatch):
    monkeypatch.delenv("AWS_REGION",raising=False)
    plan=make_study_plan("Algebra",3,1.5,"")
    assert "Day 3" in plan and "\\n" not in plan

def test_plan_validates_goal(monkeypatch):
    monkeypatch.delenv("AWS_REGION",raising=False)
    with pytest.raises(ValueError): make_study_plan("",3,1.5,"")

def test_analytics():
    assert "80%" in analyze_weak_topics([{"score":4,"total":5}])

def test_analytics_ignores_invalid_records():
    assert analyze_weak_topics([{"score":99,"total":2}]) == "Complete a valid quiz first."
