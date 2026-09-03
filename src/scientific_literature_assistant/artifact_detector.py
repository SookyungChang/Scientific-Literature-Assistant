# app/cleaning.py # text -> detect candidates
import re
import unicodedata
import json
from pprint import pprint
from scientific_literature_assistant.config import JSON_DIR
from scientific_literature_assistant.structure import detect_blocks, detect_captions, group_by_section


# ============================================================
# 1. Unicode normalization
# ============================================================

def normalize_unicode(text: str) -> str:
    """
    Normalize Unicode characters using NFC.
    """
    return unicodedata.normalize("NFC", text)


# ============================================================
# 2. Whitespace normalization
# ============================================================

def normalize_whitespace(text: str) -> str:
    """
    Normalize repeated whitespace while preserving paragraph breaks.
    """
    # spaces / tabs
    text = re.sub(r"[ \t]+", " ", text)

    # too many newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # remove spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


# ============================================================
# 3. Decimal spacing detection
# ============================================================

DECIMAL_PATTERN = re.compile(
    r"\b\d+\s+\.\s+\d+\b"
)


def detect_decimal_spacing(text: str) -> list[dict]:
    """
    Detect numbers broken by PDF extraction, e.g.
    '1 . 30' -> candidate
    '0 . 079' -> candidate
    """

    candidates = []

    for match in DECIMAL_PATTERN.finditer(text):
        candidates.append({
            "text": match.group(),
            "type": "decimal_spacing",
            "start": match.start(),
            "end": match.end(),
        })

    return candidates


# ============================================================
# 4. Line-break hyphen detection
# ============================================================

LINEBREAK_HYPHEN_PATTERN = re.compile(
    r"\b[A-Za-z]+-\n[A-Za-z]+\b"
)


def detect_linebreak_hyphen(text: str) -> list[dict]:
    """
    Detect words split by a line break:

        signifi-
        cant

    This is a candidate because the hyphen may be a PDF
    line-breaking artifact.
    """

    candidates = []

    for match in LINEBREAK_HYPHEN_PATTERN.finditer(text):
        candidates.append({
            "text": match.group(),
            "type": "linebreak_hyphen",
            "start": match.start(),
            "end": match.end(),
        })

    return candidates


# ============================================================
# 5. Suspicious token detection
# ============================================================

SUSPICIOUS_TOKEN_PATTERN = re.compile(
    r"\b[A-Za-z]{2,}(?:[A-Z][a-z]+)+\b"
)


def detect_suspicious_tokens(text: str) -> list[dict]:
    """
    Detect suspicious tokens caused by missing whitespace.

    Examples:
        'NNAissignificantly'
        'statisticsFPS'
        'humandefined'

    This only detects candidates.
    It does NOT modify the text.
    """

    candidates = []

    for match in SUSPICIOUS_TOKEN_PATTERN.finditer(text):
        candidates.append({
            "text": match.group(),
            "type": "suspicious_token",
            "start": match.start(),
            "end": match.end(),
        })

    return candidates


# ============================================================
# 6. Scientific-term spacing detection
# ============================================================

GREEK = r"αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"

SCIENTIFIC_SPACING_PATTERN = re.compile(
    rf"""
    \b
    (?:
        [A-Za-z]\s+
    )*
    [{GREEK}]
    (?:
        \s+[A-Za-z]
    )+
    \b
    """,
    re.VERBOSE
)

def detect_scientific_term_spacing(text: str) -> list[dict]:
    """
    Detect known scientific terms that have been split
    by PDF extraction.

    This is intentionally conservative.
    """

    candidates = []

    for match in SCIENTIFIC_SPACING_PATTERN.finditer(text):
        candidates.append({
            "text": match.group(),
            "type": "scientific_term_spacing",
            "start": match.start(),
                "end": match.end(),
            })

    return candidates


# ============================================================
# 7. Candidate detection pipeline
# ============================================================

def detect_candidates(text: str) -> list[dict]:
    """
    Run all deterministic candidate detectors.
    """

    candidates = []

    candidates.extend(
        detect_decimal_spacing(text)
    )

    candidates.extend(
        detect_linebreak_hyphen(text)
    )

    candidates.extend(
        detect_suspicious_tokens(text)
    )

    candidates.extend(
        detect_scientific_term_spacing(text)
    )

    # Sort by position in original text
    candidates.sort(key=lambda x: x["start"])

    return candidates

if __name__ == "__main__":
    data = json.load(open(JSON_DIR / "Chang_Human.json", encoding="utf-8"))
    results = detect_blocks(data)
    captions = detect_captions(data)
    results = group_by_section(results)
    for result in results:
        pprint(detect_candidates(result['text']))
        print()
