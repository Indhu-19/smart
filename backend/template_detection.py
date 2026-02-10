from difflib import SequenceMatcher
import re

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def fuzzy_contains(text, keyword, threshold=0.65):
    for word in text.split():
        if SequenceMatcher(None, word, keyword).ratio() >= threshold:
            return True
    return False

FORM_TEMPLATES = {

    # 🔹 MOBILE NUMBER CHANGE
    "mobile_change": {
        "signals": ["mobile", "number", "change", "update"],
        "fields": [
            "customer_name",
            "customer_id",
            "old_mobile",
            "new_mobile",
            "signature",
            "date"
        ]
    },

    # 🔹 ACCOUNT OPENING FORM
    "account_opening": {
        "signals": ["account", "opening", "open", "savings", "current"],
        "fields": [
            "customer_name",
            "father_name",
            "date_of_birth",
            "gender",
            "mobile",
            "email",
            "address",
            "city",
            "state",
            "pincode",
            "account_type",
            "nominee",
            "signature",
            "date"
        ]
    },

    # 🔹 ATM / DEBIT CARD
    "atm_card": {
        "signals": ["atm", "debit", "card"],
        "fields": [
            "customer_name",
            "account_number",
            "mobile",
            "address",
            "signature",
            "date"
        ]
    },

    # 🔹 KYC FORM
    "kyc": {
        "signals": ["kyc", "know", "customer", "identity"],
        "fields": [
            "customer_name",
            "date_of_birth",
            "aadhaar",
            "pan",
            "address",
            "signature",
            "date"
        ]
    },

    # 🔹 LOAN APPLICATION
    "loan_application": {
        "signals": ["loan", "application", "borrow"],
        "fields": [
            "customer_name",
            "father_name",
            "date_of_birth",
            "mobile",
            "email",
            "address",
            "occupation",
            "annual_income",
            "account_number",
            "signature",
            "date"
        ]
    },

    # 🔹 GOVERNMENT APPLICATION
    "govt_form": {
        "signals": ["application", "government", "scheme", "form"],
        "fields": [
            "name",
            "father_name",
            "date_of_birth",
            "aadhaar",
            "mobile",
            "address",
            "signature",
            "date"
        ]
    }
}


def detect_form_template(lines):
    full_text = normalize(" ".join(lines))
    best = None
    score = 0

    for key, tpl in FORM_TEMPLATES.items():
        matches = sum(
            fuzzy_contains(full_text, s) for s in tpl["signals"]
        )
        if matches > score:
            best = key
            score = matches

    if best and score >= 2:
        return FORM_TEMPLATES[best]

    return None
