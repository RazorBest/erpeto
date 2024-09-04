import collections
import math
import string

LOWER_ALPHA_DIGIT = string.ascii_lowercase + string.digits

def chi_squared_score(text: str, alphabet=LOWER_ALPHA_DIGIT) -> float:
    """Computes the chi squared statistic, relative to the unfiform distribution of the given alphabet.
    Ignores characters in text that are not present in the alphabet.
    """
    n = 0
    text = text.lower()
    freq: dict[str, int] = collections.defaultdict(lambda: 0)
    for c in text:
        if c in alphabet:
            n += 1

        freq[c] += 1
    
    if n == 0:
        return 0

    T = len(alphabet)
    chi = 0.0
    for c in alphabet:
        chi += freq[c]**2
    chi = chi * T / n - n

    return chi


def chi_critical_value(n, alpha=0.05):
    # https://pdfs.semanticscholar.org/c385/f52a3b4e3ae24939b3256f876048624f8b1b.pdf
    # Hoaglin's approximation of Chi squared critical value for p = 0.05
    # Verify with https://www.chisquaretable.net/
    crit = (-1.37266 + 1.06807 * math.sqrt(n) + (2.13161 - 0.04589 * math.sqrt(n)) * math.sqrt(-math.log10(alpha)))**2
    return crit

def is_random(text: str) -> bool:
    if len(text) <= 4:
        return False

    alphabet = LOWER_ALPHA_DIGIT
    chi = chi_squared_score(text, alphabet)
    n = sum(1 for c in text.lower() if c in alphabet)
    crit = chi_critical_value(n)
    if chi <= crit and n >= 4:
        return True

    alphabet = string.ascii_lowercase
    chi = chi_squared_score(text, alphabet)
    n = sum(1 for c in text.lower() if c in alphabet)
    crit = chi_critical_value(n)
    if chi <= crit and n >= 4:
        return True

    alphabet = string.digits
    chi = chi_squared_score(text, alphabet)
    n = sum(1 for c in text.lower() if c in alphabet)
    crit = chi_critical_value(n)

    return chi <= crit and n >= 4