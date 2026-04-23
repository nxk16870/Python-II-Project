

import re


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@(gmail\.com|yahoo\.com|ucmo\.edu)$")
PASSWORD_PATTERN = re.compile(
    r"^[!@#$%^&*](?=.*\d)(?=.*[a-z])(?=.*[A-Z])[A-Za-z\d!@#$%^&*]{5,11}$"
)


def validate_email(email):
    if email is None:
        return False
    return EMAIL_PATTERN.fullmatch(str(email).strip().lower()) is not None


def validate_password(password):
    if password is None:
        return False
    return PASSWORD_PATTERN.fullmatch(str(password).strip()) is not None


def get_email_requirements():
    return "Email must end in gmail.com, yahoo.com, or ucmo.edu."


def get_password_requirements():
    return (
        "Password must start with one of !@#$%^&*, be 6 to 12 characters long, "
        "and contain at least one digit, one uppercase letter, and one lowercase letter."
    )