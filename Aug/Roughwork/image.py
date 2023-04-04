
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance, ImageFilter

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def augment_image(file_path, brightness=1, contrast=1, sharpness=1, blur=0, color=0):
    img = Image.open(file_path)
    if brightness != 1:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
    if contrast != 1:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)
    if sharpness != 1:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness)
    if blur != 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    if color != 0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(color)
    return img


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            brightness = float(request.form.get('brightness', '1'))
            contrast = float(request.form.get('contrast', '1'))
            sharpness = float(request.form.get('sharpness', '1'))
            blur = float(request.form.get('blur', '0'))
            color = float(request.form.get('color', '0'))
            augmented_img = augment_image(file_path, brightness, contrast, sharpness, blur, color)
            augmented_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'augmented_' + filename)
            augmented_img.save(augmented_file_path)
            return render_template('result.html', file_path=augmented_file_path)
    return '''
    <!doctype html>
    <html lang="en">
    <head>
       <meta charset="UTF-8">
        <title>Image Augmentation</title>
        <style>
    .form-group {
        margin-bottom: 10px;
    }
    .img-container {
        max-width: 800px;
        max-height: 800px;
        overflow: auto;
        margin-top: 20px;
    }
</style>
</head>
<body>
    <h1>Image Augmentation</h1>
    <form action="/" method="POST" enctype="multipart/form-data">
        <div class="form-group">
            <label for="file">Choose Image:</label>
            <input type="file" name="file" id="file">
        </div>
        <div class="form-group">
            <label for="brightness">Brightness:</label>
            <input type="range" min="0" max="2" step="0.1" name="brightness" id="brightness" value="1">
        </div>
        <div class="form-group">
            <label for="contrast">Contrast:</label>
            <input type="range" min="0" max="2" step="0.1" name="contrast" id="contrast" value="1">
        </div>
        <div class="form-group">
            <label for="sharpness">Sharpness:</label>
            <input type="range" min="0" max="2" step="0.1" name="sharpness" id="sharpness" value="1">
        </div>
        <div class="form-group">
            <label for="blur">Blur:</label>
            <input type="range" min="0" max="10" step="0.5" name="blur" id="blur" value="0">
        </div>
        <div class="form-group">
            <label for="color">Color:</label>
            <input type="range" min="0" max="2" step="0.1" name="color" id="color" value="0">
        </div>
        <div class="form-group">
            <button type="submit">Submit</button>
        </div>
    </form>
</body>
</html>
'''


@app.route('/result')
def result():
    file_path = request.args.get('file_path')
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Augmented Image</title>
    </head>
    <body>
        <h1>Augmented Image</h1>
        <img src="{}" alt="Augmented Image">
    </body>
    </html>
    '''.format(file_path)


if __name__ == '__main__':
    app.run(debug=True)
