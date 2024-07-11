import collections
import math
import string

def randomness_score(text: str) -> float:
    """Computes the chi squared statistic, with the frequencies of the text."""
    n = 0
    text = text.lower()
    freq: dict[str, int] = collections.defaultdict(lambda: 0)
    for c in text:
        if c in string.ascii_lowercase + string.digits:
            n += 1

        freq[c] += 1

    T = len(string.ascii_lowercase + string.digits)
    chi = 0.0
    for c in string.ascii_lowercase + string.digits:
        chi += freq[c]**2
    chi = chi * T / n - n

    return chi


def is_random(text: str) -> bool:
    if len(text) <= 4:
        return False

    chi = randomness_score(text)     
    n = 0
    for c in text.lower():
        if c in string.ascii_lowercase + string.digits:
            n += 1

    # https://pdfs.semanticscholar.org/c385/f52a3b4e3ae24939b3256f876048624f8b1b.pdf
    # Hoaglin's approximation of Chi squared critical value for p = 0.05
    # Verify with https://www.chisquaretable.net/
    crit = (-1.37266 + 1.06807 * math.sqrt(n) + (2.13161 - 0.04589 * math.sqrt(n)) * math.sqrt(-math.log10(0.05)))**2

    return chi <= crit
