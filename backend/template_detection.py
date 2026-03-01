from difflib import SequenceMatcher
import re


# ================= NORMALIZE =================
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


# ================= FORM TEMPLATES =================
FORM_TEMPLATES = {

    # ================= AXIS =================

    "axis_account": {
        "signals": ["axis", "account", "opening"],
        "fields": [
            "existing_cif_id",
            "entity_name",
            "account_name",
            "existing_ckyc",

            "comm_line1", "comm_line2", "comm_city",
            "comm_state", "comm_pincode",

            "reg_line1", "reg_line2", "reg_city",
            "reg_state", "reg_pincode",

            "date_of_incorporation",
            "registration_number",
            "pan",
            "occupation_code",

            "constitution_type",

            "mobile",
            "telephone",
            "email",

            "mode_of_operation",
            "account_type",
            "initial_amount",
            "payment_mode",

            "signature",
            "date"
        ]
    },

    "axis_atm": {
        "signals": ["axis", "debit", "card"],
        "fields": [
            "account_number",
            "customer_id",
            "applicant_name",
            "mother_name",
            "date_of_birth",

            "nominee_name",
            "guardian_name",

            "mobile",
            "address",

            "card_variant",
            "reason_for_issue",

            "signature",
            "date"
        ]
    },

    # ================= BOB =================

    "bob_account": {
        "signals": ["baroda", "account", "opening"],
        "fields": [
            "branch_name",
            "account_number",

            "full_name",
            "date_of_birth",
            "pan",
            "customer_id",

            "occupation",
            "annual_income",
            "nationality",

            "father_name",

            "mobile",
            "email",

            "account_type",
            "mode_of_operation",

            "cheque_book",
            "debit_card",
            "internet_banking",

            "signature",
            "date"
        ]
    },

    "bob_atm": {
        "signals": ["baroda", "debit", "card"],
        "fields": [
            "account_number",
            "name",
            "date_of_birth",
            "gender",
            "name_on_card",

            "card_variant",
            "mobile",
            "email",

            "signature",
            "date"
        ]
    },

    "bob_mobile": {
        "signals": ["baroda", "mobile", "registration"],
        "fields": [
            "account_number",
            "pan",
            "customer_name",
            "old_mobile",
            "new_mobile",
            "date_of_birth",

            "address",

            "signature",
            "date"
        ]
    },

    # ================= HDFC =================

    "hdfc_account": {
        "signals": ["hdfc", "account", "opening"],
        "fields": [
            "application_date",
            "first_applicant_name",
            "second_applicant_name",

            "customer_id",

            "account_type",
            "currency",
            "mode_of_operation",

            "cheque_book_required",
            "debit_card_required",
            "internet_banking_required",

            "funding_mode",
            "amount",

            "beneficiary_name",

            "mobile",
            "email",

            "signature",
            "date"
        ]
    },

    "hdfc_atm": {
        "signals": ["hdfc", "atm", "debit"],
        "fields": [
            "full_name",
            "customer_id",
            "account_number",
            "card_type",

            "mobile",

            "signature",
            "date"
        ]
    },

    "hdfc_mobile": {
        "signals": ["hdfc", "mobile", "change"],
        "fields": [
            "customer_name",
            "customer_id",
            "old_mobile",
            "new_mobile",

            "signature",
            "date"
        ]
    },

    # ================= ICICI =================

    "icici_account": {
        "signals": ["icici", "account", "opening"],
        "fields": [
            "business_name",
            "date_of_incorporation",
            "place_of_incorporation",

            "ssn_or_ein",

            "mailing_address",
            "city",
            "state",
            "zip",

            "business_phone",
            "email",

            "product_type",
            "initial_deposit",

            "funding_mode",

            "signature",
            "date"
        ]
    },

    "icici_mobile": {
        "signals": ["icici", "mobile", "update"],
        "fields": [
            "service_request_number",
            "account_number",

            "name",

            "old_mobile",
            "new_mobile",

            "signature",
            "date"
        ]
    },

    # ================= INDIAN BANK =================

    "indian_account": {
        "signals": ["indian", "account", "opening"],
        "fields": [
            "cust_id",
            "branch_name",

            "full_name",
            "father_name",
            "mother_name",
            "date_of_birth",
            "gender",

            "aadhaar",
            "pan",
            "mobile",

            "occupation",
            "marital_status",

            "correspondence_address",

            "nominee_name",
            "nominee_relationship",

            "signature",
            "date"
        ]
    },

    # ================= SBI =================

    "sbi_account": {
        "signals": ["state", "bank", "india", "account"],
        "fields": [
            "branch_name",
            "customer_name",
            "date_of_birth",
            "gender",

            "address",
            "mobile",
            "email",

            "account_type",
            "mode_of_operation",

            "signature",
            "date"
        ]
    },

    "sbi_atm": {
        "signals": ["sbi", "visa", "debit"],
        "fields": [
            "branch",
            "account_number",
            "additional_account_number",

            "account_type",
            "card_request_type",

            "name_on_card",
            "address",
            "mobile",

            "father_name",
            "mother_name",

            "signature",
            "date"
        ]
    }
}


# ================= TEMPLATE DETECTION =================
def detect_form_template(lines):
    full_text = normalize(" ".join(lines))

    best_template = None
    best_score = 0

    for key, template in FORM_TEMPLATES.items():
        score = 0

        for signal in template["signals"]:
            for word in full_text.split():
                similarity = SequenceMatcher(None, word, signal).ratio()
                if similarity > 0.75:
                    score += similarity

        if score > best_score:
            best_score = score
            best_template = template

    if best_template and best_score > 1.5:
        return best_template

    return None