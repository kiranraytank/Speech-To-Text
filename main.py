from flask import Flask, render_template, request, redirect, flash, send_file
from transcriber import transcribe_short_audio, transcribe_full_audio
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')
    

@app.route('/transcribe', methods=['POST'])
def transcribe():
    print(request.files)
    print(request.form)

    if 'audiofile' not in request.files:
        flash("No file part in the request.")
        return redirect('/')

    file = request.files['audiofile']
    if file.filename == '':
        flash("No selected file.")
        return redirect('/')

    if not file.filename.lower().endswith('.wav'):
        flash("Invalid file type. Only .wav files are allowed.")
        return redirect('/')

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    action = request.form.get('action')
    if not action:
        flash("No transcription type selected.")
        return redirect('/')

    if action == 'short':
        result = transcribe_short_audio(filepath)
        title = "Short Audio Result"
    else:
        result = transcribe_full_audio(filepath)
        title = "Full Audio Result"

    return render_template("result.html", title=title, transcript=result)


@app.route('/download')
def download():
    return send_file("transcripts/transcripts.txt", as_attachment=True)

if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)
