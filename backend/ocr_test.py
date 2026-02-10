from ocr import extract_text

# 👉 change this path to the exact form image you want to test
IMAGE_PATH = "C:/Users/HP/Documents/GitHub/smart/frontend/static/forms/hdfc/mobile.jpg"
# or account.webp / atm.webp etc.

lines = extract_text(IMAGE_PATH)

print("===== RAW OCR OUTPUT =====")
for line in lines:
    print(line)
