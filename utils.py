def is_valid_email(email):
    email = email.lower()
    if "pec" in email or "legal" in email:
        return False
    return True
