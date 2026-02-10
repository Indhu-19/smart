import cv2
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    try:
        results = reader.readtext(gray)
    except:
        return []

    return [text for (_, text, _) in results if text.strip()]
