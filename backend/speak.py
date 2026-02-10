import os, time
from gtts import gTTS
from playsound import playsound
from googletrans import Translator

translator = Translator()
AUDIO_DIR = "tts_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

FIELD_PROMPTS_EN = {
    # ----- BASIC DETAILS -----
    "customer_name": "Please fill Customer Name",
    "name": "Please fill Full Name",
    "father_name": "Please fill Father's Name",
    "mother_name": "Please fill Mother's Name",
    "date_of_birth": "Please fill Date of Birth",
    "gender": "Please select Gender",

    # ----- CONTACT DETAILS -----
    "mobile": "Please fill Mobile Number",
    "old_mobile": "Please fill Old Mobile Number",
    "new_mobile": "Please fill New Mobile Number",
    "email": "Please fill Email Address",

    # ----- BANK DETAILS -----
    "account_number": "Please fill Account Number",
    "customer_id": "Please fill Customer ID",
    "branch": "Please fill Branch Name",
    "ifsc": "Please fill IFSC Code",
    "account_type": "Please select Account Type",

    # ----- KYC DETAILS -----
    "aadhaar": "Please fill Aadhaar Number",
    "pan": "Please fill PAN Number",
    "voter_id": "Please fill Voter ID Number",
    "passport": "Please fill Passport Number",

    # ----- ADDRESS -----
    "address": "Please fill Address",
    "city": "Please fill City",
    "state": "Please fill State",
    "pincode": "Please fill Pincode",

    # ----- FORMALITIES -----
    "occupation": "Please fill Occupation",
    "annual_income": "Please fill Annual Income",
    "nominee": "Please fill Nominee Name",

    # ----- END -----
    "signature": "Please sign the form",
    "date": "Please fill Date"
}


def speak(text, lang="en"):
    path = os.path.join(AUDIO_DIR, f"{int(time.time()*1000)}.mp3")
    gTTS(text=text, lang=lang).save(path)
    playsound(path)
    os.remove(path)

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

def auto_read_fields(field_list, lang="en", wait_time=0):
    for field in field_list:
        prompt = FIELD_PROMPTS_EN.get(
            field, f"Please fill {field.replace('_', ' ')}"
        )
        translate_and_speak(prompt, lang)
