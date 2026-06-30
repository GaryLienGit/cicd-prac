# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Docker!"

@app.route("/health")
def health():
    data = dict(status="healthy")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

