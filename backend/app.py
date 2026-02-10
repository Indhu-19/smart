from flask import Flask, render_template, request, session
import os, shutil

from ocr import extract_text
from intelligence import extract_fields
from template_detection import detect_form_template
from translate import translate_fields
from speak import speak_processing, announce_form, auto_read_fields

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.secret_key = "voice_form_secret"

UPLOADS = "uploads"
os.makedirs(UPLOADS, exist_ok=True)

LANG_MAP = {
    "english": "en",
    "telugu": "te",
    "hindi": "hi",
    "tamil": "ta"
}

INBUILT_FORMS = {
    "hdfc": {
        "mobile": "../frontend/static/forms/hdfc/mobile.jpg"
    }
}

@app.route("/", methods=["GET", "POST"])
def index():
    fields = {}
    error = None

    if request.method == "POST":
        input_type = request.form.get("input_type")
        image_path = os.path.join(UPLOADS, "temp.png")

        lang_name = request.form.get("language", "english").lower()
        lang = LANG_MAP.get(lang_name, "en")

        speak_processing(lang)

        # ---------- IMAGE INPUT ----------
        if input_type in ["upload", "camera"]:
            file = request.files.get("image")
            if not file or file.filename == "":
                error = "Please upload an image"
                return render_template("index.html", error=error)
            file.save(image_path)
            lines = extract_text(image_path)

        # ---------- INBUILT ----------
        elif input_type == "inbuilt":
            bank = request.form.get("bank")
            form = request.form.get("form_type")

            form_path = INBUILT_FORMS.get(bank, {}).get(form)
            if not form_path or not os.path.exists(form_path):
                error = "Inbuilt form not found"
                return render_template("index.html", error=error)

            announce_form(bank, form, lang)
            shutil.copy(form_path, image_path)
            lines = extract_text(image_path)

        else:
            error = "Invalid input type"
            return render_template("index.html", error=error)

        # ---------- TEMPLATE / INTELLIGENCE ----------
        template = detect_form_template(lines)
        if template:
            fields = {f: "" for f in template["fields"]}
        else:
            fields = extract_fields(lines)

        # ---------- SESSION STATE ----------
        session["fields"] = list(fields.keys())
        session["current_index"] = 0
        session["lang"] = lang

    return render_template("index.html", fields=fields, error=error)


@app.route("/speak/next")
def speak_next():
    fields = session.get("fields", [])
    idx = session.get("current_index", 0)
    lang = session.get("lang", "en")

    if idx < len(fields):
        auto_read_fields([fields[idx]], lang=lang, wait_time=0)
        session["current_index"] = idx + 1

    return ("", 204)


@app.route("/speak/back")
def speak_back():
    fields = session.get("fields", [])
    idx = session.get("current_index", 0)
    lang = session.get("lang", "en")

    if idx > 0:
        idx -= 1
        session["current_index"] = idx
        auto_read_fields([fields[idx]], lang=lang, wait_time=0)

    return ("", 204)


if __name__ == "__main__":
    app.run(debug=False)
