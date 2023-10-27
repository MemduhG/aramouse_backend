from flask import Flask, request, jsonify
import pyaramorph

analyzer = pyaramorph.Analyzer()


def analyze(s):
    results = analyzer.analyze_text(s)
    return results


app = Flask(__name__)


@app.route('/post_endpoint', methods=['POST'])
def post_example():
    data = request.get_data().decode("utf-8")
    analysis = analyze(data)
    return_text = ""
    print(data)
    for item in analysis:
        for line in item:
            return_text += line
        return_text += "\n"
    return jsonify(return_text.strip())


if __name__ == '__main__':
    app.run(debug=True)
