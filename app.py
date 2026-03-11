from flask import Flask, render_template, request, jsonify
import requests
import re
import os

app = Flask(__name__)

GNEWS_API_KEY = "5d296e161420e5ffee956e6a1a21649d"


def extract_keywords(text):

    stopwords = {
        "the","is","are","was","were","a","an","in","on","at",
        "today","this","that","of","for","to","and","with",
        "by","from","after","before","has","have","had"
    }

    words = re.findall(r'\w+', text.lower())

    keywords = [w for w in words if w not in stopwords]

    return " ".join(keywords[:4])


def search_news(query):

    url = f"https://gnews.io/api/v4/search?q={query}&token={GNEWS_API_KEY}&lang=en"

    response = requests.get(url)

    data = response.json()

    return data.get("articles", [])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():

    text = request.json["news"]

    # if paragraph → use first sentence
    text = text.split(".")[0]

    query = extract_keywords(text)

    articles = search_news(query)

    sources = [a["title"] for a in articles[:3]]

    if len(articles) > 0:

        prediction = "TRUE"

    else:

        prediction = "UNVERIFIED"

    return jsonify({
        "prediction": prediction,
        "sources": sources
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

