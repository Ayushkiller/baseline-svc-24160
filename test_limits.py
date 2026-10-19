from src.config import get_limit


def test_limit():
    assert get_limit("free") is not None
