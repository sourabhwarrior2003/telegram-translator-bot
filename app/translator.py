from deep_translator import GoogleTranslator
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import pycountry


# DETECT LANGUAGE
def detect_language(text: str):

    try:

        # VERY SHORT TEXT
        if len(text.strip()) < 5:
            return "Unknown"

        language_code = detect(text)

        language = pycountry.languages.get(
            alpha_2=language_code
        )

        if language:
            return language.name

        return language_code

    except LangDetectException:

        return "Unknown"

    except Exception:

        return "Unknown"


# TRANSLATE TEXT
def translate_text(
    text: str,
    target_language: str = "en"
):

    try:

        translated = GoogleTranslator(
            source="auto",
            target=target_language
        ).translate(text)

        return translated

    except Exception:

        return "Translation Error"