import re


def split_text(text):
    # Split text based on spaces while preserving punctuation marks
    words = re.findall(r"[\w']+|[.,!?;]", text)
    return words
