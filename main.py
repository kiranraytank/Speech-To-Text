from flask import Flask, render_template, request, redirect
from transcriber import transcribe_short_audio, transcribe_full_audio  # Import your functions
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audiofile' not in request.files:
        return "No file uploaded"

    file = request.files['audiofile']
    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    action = request.form['action']
    if action == 'short':
        result = transcribe_short_audio(filepath)
        title = "Short Audio Result"
    else:
        result = transcribe_full_audio(filepath)
        title = "Full Audio Result"

    return render_template("result.html", title=title, transcript=result)

if __name__ == '__main__':
    app.run(debug=True)
