import re

regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
regex_password = re.compile(r'[A-Za-z0-9@#$%^&+=]{10,}')

def check_password(password) -> bool:
    if re.fullmatch(regex_password, password):
        return True
    else:
        return False


def check_email(email) -> bool:
    if re.fullmatch(regex_email, email):
        return True
    else:
        return False
