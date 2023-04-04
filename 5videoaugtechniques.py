app.pyy----------zoomin,out,rotatecounter, counterclock, brihtness

import os
import random
import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


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
                augmentation = request.form.get('augmentation')
                if augmentation == 'zoomin':
                    for i in range(len(frames)):
                        zoom_factor = 1.5
                        zoom_center = (frame_width / 2, frame_height / 2)
                        M = cv2.getRotationMatrix2D(zoom_center, 0, zoom_factor)
                        frames[i] = cv2.warpAffine(frames[i], M, (frame_width, frame_height))
                    out_file = os.path.splitext(filename)[0] + '_zoomin.mp4'
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_file)
                    out = cv2.VideoWriter(out_path, fourcc, 20.0, (frame_width, frame_height))
                    for frame in frames:
                        out.write(frame)
                    out.release()
                    cap.release()
                    return send_from_directory(app.config['UPLOAD_FOLDER'], out_file, as_attachment=True)
                elif augmentation == 'zoomin':
                    for i in range(len(frames)):
                        zoom_factor = 1.5
                        zoom_center = (frame_width / 2, frame_height / 2)
                        M = cv2.getRotationMatrix2D(zoom_center, 0, zoom_factor)
                        frames[i] = cv2.warpAffine(frames[i], M, (frame_width, frame_height))
                    out_file = os.path.splitext(filename)[0] + '_zoomin.mp4'


                elif augmentation == 'zoomout':
                    for i in range(len(frames)):
                        zoom_factor = 0.5
                        zoom_center = (frame_width / 2, frame_height / 2)
                        M = cv2.getRotationMatrix2D(zoom_center, 0, zoom_factor)
                        frames[i] = cv2.warpAffine(frames[i], M, (frame_width, frame_height))
                    out_file = os.path.splitext(filename)[0] + '_zoomout.mp4'
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_file)
                    out = cv2.VideoWriter(out_path, fourcc, 20.0, (frame_width, frame_height))
                    for frame in frames:
                        out.write(frame)
                    out.release()
                    cap.release()
                    return send_from_directory(app.config['UPLOAD_FOLDER'], out_file, as_attachment=True)
                elif augmentation == 'zoomout':
                    for i in range(len(frames)):
                        zoom_factor = 0.5
                        zoom_center = (frame_width / 2, frame_height / 2)
                        M = cv2.getRotationMatrix2D(zoom_center, 0, zoom_factor)
                        frames[i] = cv2.warpAffine(frames[i], M, (frame_width, frame_height))
                    out_file = os.path.splitext(filename)[0] + '_zoomout.mp4'
                # elif augmentation == 'rotatecw':
                #     for i in range(len(frames)):
                #         frames[i] = cv2.rotate(frames[i], cv2.ROTATE_90_CLOCKWISE)
                #     out_file = os.path.splitext(filename)[0] + '_rotatecw.mp4'
                # elif augmentation == 'rotateccw':
                #     for i in range(len(frames)):
                #         frames[i] = cv2.rotate(frames[i], cv2.ROTATE_90_COUNTERCLOCKWISE)
                #     out_file = os.path.splitext(filename)[0] + '_rotateccw.mp4'

                elif augmentation == 'rotatecw':
                    for i in range(len(frames)):
                        frames[i] = cv2.rotate(frames[i], cv2.ROTATE_90_CLOCKWISE)
                    out_file = os.path.splitext(filename)[0] + '_rotatecw.mp4'
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_file)
                    out = cv2.VideoWriter(out_path, fourcc, 20.0, (frame_width, frame_height))
                    for frame in frames:
                        out.write(cv2.transpose(frame))
                    out.release()
                    cap.release()
                    return send_from_directory(app.config['UPLOAD_FOLDER'], out_file, as_attachment=True)

                elif augmentation == 'rotateccw':
                    for i in range(len(frames)):
                        frames[i] = cv2.rotate(frames[i], cv2.ROTATE_90_COUNTERCLOCKWISE)
                    out_file = os.path.splitext(filename)[0] + '_rotateccw.mp4'
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_file)
                    out = cv2.VideoWriter(out_path, fourcc, 20.0, (frame_width, frame_height))
                    for frame in frames:
                        out.write(cv2.transpose(frame))
                    out.release()
                    cap.release()
                    return send_from_directory(app.config['UPLOAD_FOLDER'], out_file, as_attachment=True)

                elif augmentation == 'brightness':
                    brightness_factor = random.uniform(0.5,
                                                       3.5)  # adjust brightness by a random factor between 0.5 and 1.5
                    for i in range(len(frames)):
                        hsv = cv2.cvtColor(frames[i], cv2.COLOR_BGR2HSV)
                        h, s, v = cv2.split(hsv)
                        v = cv2.multiply(v, brightness_factor)
                        v = np.clip(v, 0, 255).astype(np.uint8)
                        hsv = cv2.merge((h, s, v))
                        frames[i] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
                    out_file = os.path.splitext(filename)[0] + '_brightness.mp4'
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_file)
                    out = cv2.VideoWriter(out_path, fourcc, 20.0, (frame_width, frame_height))
                    for frame in frames:
                        out.write(frame)
                    out.release()
                    cap.release()
                    return send_from_directory(app.config['UPLOAD_FOLDER'], out_file, as_attachment=True)


                else:
                    return render_template('error.html', message='Invalid augmentation selected')

                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_file)
                out = cv2.VideoWriter(out_path, fourcc, 20.0, (frame_height, frame_width))
                for frame in frames:
                    out.write(frame)
                out.release()
                cap.release()

                # send the output file for download
                return send_from_directory(app.config['UPLOAD_FOLDER'], out_file, as_attachment=True)
            else:
                return render_template('error.html', message='Video not opened successfully')
    return render_template('augment.html')


def write_video(frames, out_path, frame_width, frame_height):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 20.0, (frame_width, frame_height))
    for frame in frames:
        out.write(frame)
    out.release()


if __name__ == '__main__':
    app.run(debug=True, port=3030)






    index---

    <!DOCTYPE html>
<html>
<head>
    <title>Video Augmentation</title>
</head>
<body>
    <h1>Video Augmentation</h1>
    <p>Select a video file to augment:</p>
    <form action="{{ url_for('augment') }}" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="video/*">
        <br><br>
        <label for="augmentation">Choose an augmentation:</label>
        <select name="augmentation" id="augmentation">
            <option value="zoomin">Zoom In</option>
            <option value="zoomout">Zoom Out</option>
            <option value="rotatecw">Rotate Clockwise</option>
            <option value="rotateccw">Rotate Counter-Clockwise</option>
            <option value="brightness">Change Brightness </option>
        </select>
        <br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>




augment---

<!DOCTYPE html>
<html>
<head>
    <title>Video Augmentation</title>
</head>
<body>
    <h1>Video Augmentation</h1>
    <p>Select a video file to augment:</p>
    <form action="{{ url_for('augment') }}" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="video/*">
        <br><br>
        <label for="augmentation">Choose an augmentation:</label>
        <select name="augmentation" id="augmentation">
            <option value="zoomin">Zoom In</option>
            <option value="zoomout">Zoom Out</option>
            <option value="rotatecw">Rotate Clockwise</option>
            <option value="rotateccw">Rotate Counter-Clockwise</option>
            <option value="brightness">Change Brightness </option>
        </select>
        <br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>

