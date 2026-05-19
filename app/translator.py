# translation functions
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
import pycountry

def get_language_name(code: str) -> str:
    try:
        language = pycountry.languages.get(alpha_2=code)
        return language.name if language else code
    except:
        return code

def get_flag_emoji(code: str) -> str:
    try:
        country_code = code.upper()
        return ''.join(chr(127397 + ord(c)) for c in country_code)
    except:
        return ""

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def translate_text(text: str) -> dict:
    detected_code = detect_language(text)
    language_name = get_language_name(detected_code)
    flag = get_flag_emoji(detected_code)

    translated = GoogleTranslator(
        source="auto",
        target="en"
    ).translate(text)

    return {
        "detected_code": detected_code,
        "language_name": language_name,
        "flag": flag,
        "translated_text": translated
    }
