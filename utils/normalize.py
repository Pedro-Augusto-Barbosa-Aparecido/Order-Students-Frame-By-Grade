import unicodedata


def remove_accents(string: str):
    string = unicodedata.normalize('NFKD', string)
    return "".join(
        [
            c for c in string if not unicodedata.combining(c)
        ]
    )
