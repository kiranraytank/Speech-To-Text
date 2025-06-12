from flask import Flask, render_template, request
from transcriber import transcribe_short_audio, transcribe_full_audio  # Import your functions

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_short_transcription')
def run_short():
    result = transcribe_short_audio("short_sample.wav")
    return render_template("result.html", title="Short Audio Result", transcript=result)

@app.route('/run_full_transcription')
def run_full():
    result = transcribe_full_audio("long_sample.wav")
    return render_template("result.html", title="Full Audio Result", transcript=result)

if __name__ == '__main__':
    app.run(debug=True)