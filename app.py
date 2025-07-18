from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROTECTED_FOLDER = 'protected'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROTECTED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf']
        password = request.form['password']

        if file.filename == '' or password == '':
            return "Please upload a PDF and enter a password."

        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(user_password=password, owner_password=password)

        protected_path = os.path.join(PROTECTED_FOLDER, 'protected_' + filename)
        with open(protected_path, 'wb') as f:
            writer.write(f)

        return send_file(protected_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
