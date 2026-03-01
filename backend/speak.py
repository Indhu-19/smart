import os
import time
from gtts import gTTS
from playsound import playsound
from googletrans import Translator

translator = Translator()

AUDIO_DIR = "tts_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

FIELD_PROMPTS_EN = {

    # ===== Generic =====
    "signature": "Please provide your signature.",
    "date": "Please enter the date.",

    # ===== Identity =====
    "full_name": "Please enter your full name.",
    "customer_name": "Please enter the customer name.",
    "applicant_name": "Please enter the applicant name.",
    "first_applicant_name": "Please enter the first applicant name.",
    "second_applicant_name": "Please enter the second applicant name.",
    "father_name": "Please enter your father's name.",
    "mother_name": "Please enter your mother's name.",
    "date_of_birth": "Please enter your date of birth.",
    "gender": "Please select your gender.",

    # ===== ID Numbers =====
    "existing_cif_id": "Please enter the existing CIF ID.",
    "customer_id": "Please enter the customer ID.",
    "registration_number": "Please enter the registration number.",
    "account_number": "Please enter the account number.",
    "additional_account_number": "Please enter the additional account number.",
    "pan": "Please enter the PAN number.",
    "aadhaar": "Please enter the Aadhaar number.",
    "ssn_or_ein": "Please enter the SSN or EIN number.",
    "service_request_number": "Please enter the service request number.",

    # ===== Contact =====
    "mobile": "Please enter your mobile number.",
    "old_mobile": "Please enter your old mobile number.",
    "new_mobile": "Please enter your new mobile number.",
    "telephone": "Please enter your telephone number.",
    "email": "Please enter your email address.",
    "business_phone": "Please enter the business phone number.",

    # ===== Address =====
    "address": "Please enter your address.",
    "mailing_address": "Please enter your mailing address.",
    "correspondence_address": "Please enter your correspondence address.",
    "comm_line1": "Please enter Communication Address Line 1.",
    "comm_line2": "Please enter Communication Address Line 2.",
    "comm_city": "Please enter Communication City.",
    "comm_state": "Please enter Communication State.",
    "comm_pincode": "Please enter Communication Pincode.",
    "reg_line1": "Please enter Registered Address Line 1.",
    "reg_line2": "Please enter Registered Address Line 2.",
    "reg_city": "Please enter Registered City.",
    "reg_state": "Please enter Registered State.",
    "reg_pincode": "Please enter Registered Pincode.",
    "city": "Please enter the city.",
    "state": "Please enter the state.",
    "zip": "Please enter the ZIP code.",

    # ===== Business Details =====
    "entity_name": "Please enter the entity name.",
    "account_name": "Please enter the account name.",
    "business_name": "Please enter the business name.",
    "date_of_incorporation": "Please enter the date of incorporation.",
    "place_of_incorporation": "Please enter the place of incorporation.",
    "occupation": "Please enter your occupation.",
    "occupation_code": "Please enter the occupation code.",
    "annual_income": "Please enter the annual income.",
    "nationality": "Please enter the nationality.",
    "constitution_type": "Please select the constitution type.",
    "marital_status": "Please select the marital status.",

    # ===== Banking Details =====
    "account_type": "Please select the account type.",
    "mode_of_operation": "Please select the mode of operation.",
    "currency": "Please select the currency.",
    "initial_amount": "Please enter the initial deposit amount.",
    "initial_deposit": "Please enter the initial deposit amount.",
    "amount": "Please enter the amount.",
    "funding_mode": "Please select the funding mode.",
    "payment_mode": "Please select the payment mode.",
    "cheque_number": "Please enter the cheque number.",
    "debit_account_number": "Please enter the debit account number.",
    "branch_name": "Please enter the branch name.",

    # ===== ATM / Card =====
    "card_type": "Please select the card type.",
    "card_variant": "Please select the card variant.",
    "card_request_type": "Please select the card request type.",
    "name_on_card": "Please enter the name to be printed on the card.",
    "reason_for_issue": "Please select the reason for card request.",

    # ===== Nominee =====
    "nominee_name": "Please enter the nominee name.",
    "nominee_relationship": "Please enter the nominee relationship.",
    "guardian_name": "Please enter the guardian name.",

    # ===== Banking Services =====
    "mobile_banking": "Do you require mobile banking?",
    "internet_banking": "Do you require internet banking?",
    "internet_banking_required": "Do you require internet banking?",
    "sms_alert": "Do you require SMS alerts?",
    "cheque_book_required": "Do you require a cheque book?",
    "debit_card_required": "Do you require a debit card?",

}

def speak(text, lang="en"):
    try:
        print("Speaking:", text)

        filename = f"speech_{int(time.time()*1000)}.mp3"
        path = os.path.join(AUDIO_DIR, filename)

        tts = gTTS(text=text, lang=lang)
        tts.save(path)

        playsound(path)

        time.sleep(0.5)  # Prevent instant deletion issue
        os.remove(path)

    except Exception as e:
        print("Speech Error:", e)


def translate_and_speak(text_en, lang):
    if lang != "en":
        try:
            text_en = translator.translate(text_en, dest=lang).text
        except:
            pass
    speak(text_en, lang)


def speak_processing(lang="en"):
    translate_and_speak("Processing the form. Please wait.", lang)


def announce_form(bank, form, lang="en"):
    translate_and_speak(f"{bank.upper()} {form} form detected", lang)


def auto_read_fields(field_list, lang="en"):
    for field in field_list:
        prompt = FIELD_PROMPTS_EN.get(
            field,
            f"Please fill {field.replace('_', ' ')}"
        )
        translate_and_speak(prompt, lang)
