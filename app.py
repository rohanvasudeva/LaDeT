from flask import Flask, render_template, request, redirect, url_for
from langdetect import detect
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES

app = Flask(__name__)

# Convert {"english":"en"} -> {"en":"English"}
LANGUAGES = {code: name.title() for name, code in GOOGLE_LANGUAGES_TO_CODES.items()}


def detect_and_translate(text, target_lang):
    # Detect language
    detected_lang = detect(text)

    # Translate text
    translated_text = GoogleTranslator(
        source='auto',
        target=target_lang
    ).translate(text)

    return detected_lang, translated_text


@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)


@app.route('/trans', methods=['POST'])
def trans():
    translation = ""
    detected_lang = ""

    if request.method == 'POST':
        text = request.form['text']
        target_lang = request.form['target_lang']

        detected_lang, translation = detect_and_translate(text, target_lang)

    return render_template(
        'index.html',
        translation=translation,
        detected_lang=detected_lang,
        languages=LANGUAGES
    )


if __name__ == '__main__':
    app.run(debug=True)