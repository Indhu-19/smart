from flask import Flask, render_template, request, session, jsonify
import os

from ocr import extract_text
from intelligence import extract_fields
from template_detection import detect_form_template, FORM_TEMPLATES
from speak import speak_processing, auto_read_fields, announce_form

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


@app.route("/", methods=["GET", "POST"])
def index():
    fields = {}
    error = None

    if request.method == "POST":

        image_path = os.path.join(UPLOADS, "temp.png")

        input_type = request.form.get("input_type", "upload")
        bank = request.form.get("bank")
        form_type = request.form.get("form_type")

        lang_name = request.form.get("language", "english").lower()
        lang = LANG_MAP.get(lang_name, "en")

        speak_processing(lang)

        # ================= UPLOAD MODE =================
        if input_type == "upload":

            file = request.files.get("image")

            if file and file.filename != "":
                file.save(image_path)

                lines = extract_text(image_path, lang)

                template = detect_form_template(lines)

                if template:
                    fields = {f: "" for f in template["fields"]}
                else:
                    fields = extract_fields(lines)

                if not fields:
                    error = "No fields detected. Try clearer image."
            else:
                error = "Please upload an image."

        # ================= INBUILT MODE =================
        elif input_type == "inbuilt":

            if not bank or not form_type:
                error = "Please select bank and form type."
            else:
                template_key = f"{bank}_{form_type}"

                if template_key in FORM_TEMPLATES:
                    template = FORM_TEMPLATES[template_key]
                    fields = {f: "" for f in template["fields"]}
                    session["template_key"] = template_key

                    announce_form(bank.upper(), form_type.upper(), lang)
                else:
                    error = "Invalid form selection."

        # ================= SESSION SETUP =================
        if fields:
            session["fields"] = list(fields.keys())
            session["current_index"] = 0
            session["lang"] = lang
            session["form_data"] = {}

    return render_template(
        "index.html",
        fields=fields,
        error=error,
        form_data=session.get("form_data", {})
    )


@app.route("/speak/next")
def speak_next():
    fields = session.get("fields", [])
    idx = session.get("current_index", 0)
    lang = session.get("lang", "en")

    if idx < len(fields):
        field = fields[idx]
        auto_read_fields([field], lang=lang)
        session["current_index"] = idx + 1
        return jsonify({"field": field})

    return jsonify({"field": None})


@app.route("/speak/back")
def speak_back():
    fields = session.get("fields", [])
    idx = session.get("current_index", 0)
    lang = session.get("lang", "en")

    if idx > 0:
        idx -= 1
        session["current_index"] = idx
        auto_read_fields([fields[idx]], lang=lang)
        return jsonify({"field": fields[idx]})

    return jsonify({"field": None})


@app.route("/save_field", methods=["POST"])
def save_field():
    data = request.get_json()

    field = data.get("field")
    value = data.get("value")

    if not field:
        return jsonify({"status": "error"})

    form_data = session.get("form_data", {})
    form_data[field] = value
    session["form_data"] = form_data

    return jsonify({"status": "saved"})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)