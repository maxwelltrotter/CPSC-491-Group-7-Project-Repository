import re


def check_password(password):
    """Return a list of problems. An empty list means the password is fine."""
    if not isinstance(password, str):
        return ["Password must be text."]

    problems = []
    if len(password) < 8:
        problems.append("Password must be at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        problems.append("Password needs an uppercase letter.")
    if not re.search(r"[a-z]", password):
        problems.append("Password needs a lowercase letter.")
    if not re.search(r"\d", password):
        problems.append("Password needs a number.")
    if not re.search(r"[^A-Za-z0-9]", password):
        problems.append("Password needs a special character.")
    return problems