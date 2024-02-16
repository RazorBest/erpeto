import collections
import string


def randomness_score(text: str) -> float:
    """Computes the chi squared statistic, with the frequencies of the text."""
    if len(text) <= 3:
        return 0

    text = text.lower()
    freq: dict[str, int] = collections.defaultdict(lambda: 0)
    for c in text:
        freq[c] += 1

    n = len(text)
    chi = 0.0
    T = len(string.ascii_lowercase + string.digits)
    for c in string.ascii_lowercase + string.digits:
        chi += freq[c] ** 2
    chi = chi * T / n
    chi -= n

    return chi
