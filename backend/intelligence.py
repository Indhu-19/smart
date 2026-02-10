import re
from difflib import get_close_matches
from utils import clean_text

FIELD_KEYWORDS = {
    "name": ["name", "nane"],
    "phone": ["phone", "mobile"],
    "aadhaar": ["aadhaar", "aadhar"],
    "address": ["address"],
    "email": ["email", "mail"],
    "pan": ["pan"],
    "ifsc": ["ifsc"],
    "account_number": ["account", "acc"],
    "date_of_birth": ["dob", "birth"],
    "pincode": ["pin", "pincode"]

}

REGEX_PATTERNS = {
    "phone": r"\b\d{10}\b",
    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b"
}

def fuzzy_match(word, keywords):
    return get_close_matches(word, keywords, n=1, cutoff=0.75)

def extract_fields(lines):
    fields = {}

    for line in lines:
        clean_line = clean_text(line)

        for field, pattern in REGEX_PATTERNS.items():
            if field not in fields:
                match = re.search(pattern, clean_line)
                if match:
                    fields[field] = match.group()

        for field, keywords in FIELD_KEYWORDS.items():
            if field in fields:
                continue
            for word in clean_line.split():
                if fuzzy_match(word, keywords):
                    value = clean_line.replace(word, "").strip()
                    if value:
                        fields[field] = value

    return fields
