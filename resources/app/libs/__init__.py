import unicodedata

from .logger import Logger

def strip_accents(text):
    try:
        text = unicode(text, "utf-8")
    except NameError:  # unicode is a default on python 3
        pass

    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")

    return str(text)


def get_more_similar_str(needle: str, list_to_compare: list[str]) -> str:
    """Get the most similar string from a list of strings."""
    from difflib import SequenceMatcher

    str = strip_accents(needle.upper())
    list = [strip_accents(s.upper()) for s in list_to_compare]
    return max(list, key=lambda s: SequenceMatcher(None, str, s).ratio())
