from flask import Flask, render_template
from utils import text_to_html_spans

verse = "وَلَا تَحْسَبَنَّ الَّذِينَ قُتِلُوا فِي سَبِيلِ اللَّهِ أَمْوَاتًا ۚ بَلْ أَحْيَاءٌ عِندَ رَبِّهِمْ يُرْزَقُونَ (169)"
app = Flask(__name__)


@app.route("/")
def index():
    (
        html_content,
        tokens_count,
        total_diacritics,
        wd_dict,
        char_dict_global,
        char_dict_local,
    ) = text_to_html_spans(verse)

    return render_template(
        "ui_diacriticizer.html",
        injected_content=html_content,
        verse=html_content,
        tokens_count=tokens_count,
        total_diacritics=total_diacritics,
        wd_dict=wd_dict,
        char_dict_global=char_dict_global,
        char_dict_local=char_dict_local,
    )


if __name__ == "__main__":
    app.run(debug=True)
