import re


def check_password_security(password: str) -> bool:
    length = len(password)
    digits = re.search(r"\d+", password)
    uppercase = re.search(r"[A-Z]+", password)
    lowercase = re.search(r"[a-z]+", password)
    special_symbols = re.search(r"[^A-Za-z0-9]+", password)

    flag = True

    while True:
        if length < 8:
            print("The password length must be more than 8 symbols")
        if not digits:
            print("Your password should include digits")
        if not uppercase:
            print("Your password has to contain uppercase letters")
        if not lowercase:
            print("Your password has to contain lowercase letters")
        if not special_symbols:
            print("Your password has to contain special symbols")
            break

    return (
        False
        if any(i is True for i in (length, not digits, not uppercase, not lowercase, not special_symbols))
        else True
    )
