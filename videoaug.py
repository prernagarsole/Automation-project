app.py --
import cv2
import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp4'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/augment', methods=['GET', 'POST'])
def augment():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('error.html', message='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('error.html', message='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            cap = cv2.VideoCapture(file_path)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))

            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)

            if cap.isOpened():
                for i in range(len(frames)):
                    zoom_factor = 1.5
                    zoom_center = (frame_width / 2, frame_height / 2)
                    M = cv2.getRotationMatrix2D(zoom_center, 0, zoom_factor)
                    frames[i] = cv2.warpAffine(frames[i], M, (frame_width, frame_height))
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out_file = os.path.splitext(filename)[0] + '_zoomin.mp4'
                out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_file)
                out = cv2.VideoWriter(out_path, fourcc, 20.0, (frame_width, frame_height))
                for frame in frames:
                    out.write(frame)
                out.release()
                cap.release()
                return send_from_directory(app.config['UPLOAD_FOLDER'], out_file, as_attachment=True)
            else:
                return render_template('error.html', message='Video not opened successfully')
    return render_template('augment.html')


if __name__ == '__main__':
    app.run(debug=True)






    index---


    
<!DOCTYPE html>
<html>
<head>
    <title>Video Augment</title>
</head>
<body>
    <form action="/augment" method="post" enctype="multipart/form-data">
        <label for="file">Select a video to augment:</label>
        <input type="file" id="file" name="file" accept="video/mp4"><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>




augment

<!DOCTYPE html>
<html>
<head>
    <title>Video Augment</title>
</head>
<body>
    {% if message %}
        <p style="color: red">{{ message }}</p>
    {% endif %}
    <form action="/augment" method="post" enctype="multipart/form-data">
        <label for="file">Select a video to augment:</label>
        <input type="file" id="file" name="file" accept="video/mp4"><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>


