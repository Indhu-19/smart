from googletrans import Translator

translator = Translator()

def translate_fields(fields, lang):
    translated = {}
    for k, v in fields.items():
        try:
            translated[k] = translator.translate(v, dest=lang).text
        except:
            translated[k] = v
    return translated
