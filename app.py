from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
import g4f

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    essay = ""
    if request.method == 'POST':
        user_text = request.form.get('text')
        # 1. Tarjima
        result = GoogleTranslator(source='auto', target='en').translate(user_text)

        # 2. AI Insho (agar foydalanuvchi "insho:" deb yozsa)
        if user_text.lower().startswith("insho:"):
            try:
                essay = g4f.ChatCompletion.create(
                    model=g4f.models.default,
                    messages=[{"role": "user", "content": f"{user_text} haqida o'zbekcha insho yoz"}],
                )
            except:
                essay = "AI hozirda band, keyinroq urinib ko'ring."

    return render_template('index.html', result=result, essay=essay)


if __name__ == '__main__':
    app.run(debug=True)