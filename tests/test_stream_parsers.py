import pytest
from datetime import datetime
from pydantic import ValidationError
from stellar_harvest_ie_consumers.stream_parsers import parse_planetary_kp_index


@pytest.fixture(scope="class")
def sample_planetary_kp_index():
    return {
        "time_tag": "2025-05-17T12:16:00",
        "kp_index": 1,
        "estimated_kp": 1.33,
        "kp": "1P",
    }


def test_parse_planetary_kp_index(sample_planetary_kp_index):
    parsed = parse_planetary_kp_index(sample_planetary_kp_index)

    assert isinstance(parsed["time_tag"], datetime)
    assert parsed["time_tag"] == datetime(2025, 5, 17, 12, 16, 0)
    assert parsed["kp_index"] == 1
    assert parsed["estimated_kp"] == pytest.approx(1.33)
    assert parsed["kp"] == "1P"


def test_parse_pl_kp_idx_missing_kp_index(sample_planetary_kp_index):
    sample = sample_planetary_kp_index.copy()
    sample.pop("kp_index")
    with pytest.raises(ValidationError):
        parse_planetary_kp_index(sample)


def test_parse_pl_kp_idx_ignores_extra_fields(sample_planetary_kp_index):
    sample = sample_planetary_kp_index.copy()
    sample["foo"] = "bar"
    parsed = parse_planetary_kp_index(sample)
    assert "foo" not in parsed
