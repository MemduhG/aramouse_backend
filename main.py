import json

from flask import Flask, request, jsonify, render_template
import pyaramorph

analyzer = pyaramorph.Analyzer()


def analyze(s):
    results = analyzer.analyze_text(s)
    return results


app = Flask(__name__)

with open("static/translit.json") as infile:
    translit_dict = json.load(infile)


@app.route('/')
def index():
    return render_template('index.html')


def translit(text):
    transliterated = ""
    for char in text:
        if char in translit_dict:
            transliterated += translit_dict[char]
        else:
            transliterated += char

    return transliterated


def analyze_text(inp):
    text = translit(inp)
    print(text)
    analysis = analyze(text)
    print(analysis)
    return_list = []
    for item in analysis:
        item_list = []
        for line in item:
            item_list.append(line)

        if len(item_list) > 0:
            return_list.append(item_list)
    return jsonify({"analyzed_text": return_list})


@app.route('/post_endpoint', methods=['POST'])
def post_example():
    data = request.get_data().decode("utf-8")
    return analyze_text(data)


@app.route('/html_endpoint', methods=['POST'])
def post_html():
    data = json.loads(request.get_data().decode("utf-8"))
    return analyze_text(data["text"])


if __name__ == '__main__':
    app.run(debug=True)
