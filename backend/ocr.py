import cv2
import easyocr


def extract_text(image_path, lang="en"):

    # 🔹 EasyOCR language mapping
    lang_map = {
        "en": ["en"],
        "te": ["te", "en"],
        "hi": ["hi", "en"],
        "ta": ["ta", "en"]
    }

    selected_lang = lang_map.get(lang, ["en"])

    reader = easyocr.Reader(selected_lang, gpu=False)

    img = cv2.imread(image_path)

    if img is None:
        print("Image not loaded:", image_path)
        return []

    # 🔹 Improved preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise removal
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Adaptive threshold (better for forms)
    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    try:
        results = reader.readtext(gray)
    except Exception as e:
        print("OCR Error:", e)
        return []

    texts = [text for (_, text, _) in results if text.strip()]

    print("OCR Extracted:", texts)

    return texts