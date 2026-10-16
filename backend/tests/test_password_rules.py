from app.validators import check_password


def test_strong_password_passes():
    assert check_password("Abcdef1!") == []


def test_too_short_fails():
    assert check_password("Ab1!") != []


def test_missing_uppercase_fails():
    assert check_password("abcdef1!") != []


def test_missing_lowercase_fails():
    assert check_password("ABCDEF1!") != []


def test_missing_number_fails():
    assert check_password("Abcdefg!") != []


def test_missing_special_character_fails():
    assert check_password("Abcdefg1") != []


def test_non_text_fails():
    assert check_password(None) != []