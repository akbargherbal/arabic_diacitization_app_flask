from flask import Flask, render_template, url_for
from utils import text_to_html_spans

verse = "وَلَا تَحْسَبَنَّ الَّذِينَ قُتِلُوا فِي سَبِيلِ اللَّهِ أَمْوَاتًا ۚ بَلْ أَحْيَاءٌ عِندَ رَبِّهِمْ يُرْزَقُونَ (169)"
# For demonstration, add a second verse to serve on the "next" request
next_verse = (
    "الَّذِينَ يَذْكُرُونَ اللَّهَ قِيَامًا وَقُعُودًا وَعَلَىٰ جُنُوبِهِمْ وَيَتَفَكَّرُونَ فِي خَلْقِ السَّمَاوَاتِ وَالْأَرْضِ"
)

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
        # This part is correct because ui_diacriticizer.html aliases this variable
        injected_content=html_content,
        tokens_count=tokens_count,
        total_diacritics=total_diacritics,
        wd_dict=wd_dict,
        char_dict_global=char_dict_global,
        char_dict_local=char_dict_local,
    )


# ADD THIS NEW HTMX ENDPOINT
@app.route("/save-and-next", methods=["POST"])
def save_and_next():
    """
    This endpoint handles the HTMX request.
    It returns ONLY the updated sentence partial, not the full page.
    """
    # In a real application, you would save the previous state and fetch
    # the next verse from a database. Here, we just use our second verse.

    # --- FIX #1: Use `next_verse` instead of `verse` ---
    (
        html_content,
        tokens_count,
        total_diacritics,
        wd_dict,
        char_dict_global,
        char_dict_local,
    ) = text_to_html_spans(next_verse)

    # Render the SAME partial, but pass a flag to it.
    # --- FIX #2: Pass the HTML content as `custom_html` to match the template ---
    return render_template(
        "partials/sentence.html",
        custom_html=html_content,  # CORRECTED VARIABLE NAME
        # The rest of these are needed by the script block in sentence.html
        tokens_count=tokens_count,
        total_diacritics=total_diacritics,
        wd_dict=wd_dict,
        char_dict_global=char_dict_global,
        char_dict_local=char_dict_local,
        is_htmx_update=True,
    )


if __name__ == "__main__":
    app.run(debug=True)
