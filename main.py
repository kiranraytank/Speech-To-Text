from flask import Flask, render_template, request, redirect, flash, make_response
from transcriber import transcribe_short_audio, transcribe_full_audio
from transformers import T5Tokenizer, T5ForConditionalGeneration
from fpdf import FPDF  # Make sure to install: pip install fpdf
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # Load T5 summarization model and tokenizer
# tokenizer = T5Tokenizer.from_pretrained("t5-small")
# model = T5ForConditionalGeneration.from_pretrained("t5-small")

def summarize_text(text):
    input_text = "summarize: " + text.strip()
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(input_ids, max_length=100, min_length=30, length_penalty=5.0, num_beams=2)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


from flask import make_response
from fpdf import FPDF
import re

def remove_emojis(text):
    # Removes emojis and other non-latin-1 characters
    return re.sub(r'[^\x00-\xFF]', '', text)


@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    transcript = request.form.get('transcript', '')
    summary = request.form.get('summary', '')
    filename = request.form.get('filename', 'transcript')

    try:
        transcript_clean = remove_emojis(transcript)
        summary_clean = remove_emojis(summary)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, "Full Transcript:\n" + transcript_clean)
        pdf.ln(5)
        pdf.multi_cell(0, 10, "Transcript Summary:\n" + summary_clean)

        pdf_name = f"{filename}.pdf"
        response = make_response(pdf.output(dest='S').encode('latin1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={pdf_name}'
        return response

    except Exception as e:
        return f"PDF Generation Failed: {str(e)}", 500


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
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

    filename_var = os.path.splitext(file.filename)[0] 
    
    # ✅ Check for error message
    if "No speech recognized." in result:
        summary = ""
        allow_pdf = False
    else:
        # summary = summarize_text(result)
        # sometime STOP to this code run
        summary = ""
        allow_pdf = True

    return render_template("result.html", title=title, transcript=result, summary=summary, filename=filename_var, allow_pdf=allow_pdf)

@app.route('/healthz')
def health_check():
    return "OK", 200


# if __name__ == '__main__':
#     app.secret_key = 'RayTank343mddsnfdsn'
#     app.run(debug=True)

if __name__ == '__main__':
    app.secret_key = os.environ.get("SECRET_KEY", "RayTank343mddsnfdsn")
    port = int(os.environ.get('PORT', 5000))  # Use Render's port or default to 5000
    app.run(host='0.0.0.0', port=port)
    