from flask import Flask, request, Response
from io import BytesIO
from gtts import gTTS
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <html>
            <head>
                <title>Text to Speech Converter</title>
                <style>
                    body {
                        font-family: sans-serif;
                    }
                    label {
                        font-weight: bold;
                    }
                    textarea {
                        width: 100%;
                        height: 100px;
                    }
                    #audio-container {
                        margin-top: 20px;
                    }
                    #audio-player {
                        width: 100%;
                    }
                    #download-link {
                        margin-top: 10px;
                    }
                </style>
            </head>
            <body>
                <form method="POST" action="/convert">
                    <label for="text">Enter text:</label>
                    <textarea name="text" id="text" placeholder="Enter your text here..."></textarea>
                    <br/>
                    <label for="languages">Select languages:</label>
                    <select name="languages" id="languages" multiple>
                        <option value="en">English</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                        <option value="es">Spanish</option>
                    </select>
                    <br/>
                    <label for="speeds">Select speeds:</label>
                    <select name="speeds" id="speeds" multiple>
                        <option value="slow">Slow</option>
                        <option value="normal" selected>Normal</option>
                        <option value="fast">Fast</option>
                    </select>
                    <br/>
                    <button type="submit">Convert to audio</button>
                </form>
                <div id="audio-container"></div>
            </body>
        </html>
    '''


@app.route('/convert', methods=['POST'])
@app.route('/convert', methods=['POST'])
@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    languages = request.form.getlist('languages')
    speeds = request.form.getlist('speeds')
    audio_elements = ""
    for language in languages:
        for speed in speeds:
            audio = gTTS(text=text, lang=language, slow=speed == 'slow')
            audio_file = BytesIO()
            audio.write_to_fp(audio_file)
            audio_file.seek(0)
            audio_data = base64.b64encode(audio_file.getvalue()).decode('utf-8')
            audio_element = '<audio id="audio-player" controls><source src="data:audio/mp3;base64,{}" type="audio/mp3"></audio>'.format(
                audio_data)
            language_label = {'en': 'English', 'fr': 'French', 'de': 'German', 'es': 'Spanish'}[language]
            speed_label = {'slow': 'Slow', 'normal': 'Normal', 'fast': 'Fast'}[speed]
            download_label = '{}_{}_{}.mp3'.format(language_label, speed_label, text[:10])
            download_link = '<a id="download-link" href="data:audio/mp3;base64,{}" download="{}">Download audio</a>'.format(
                audio_data, download_label)
            audio_elements += '<p>{}, {}:</p>{}<br/>{}'.format(language_label, speed_label, audio_element,
                                                               download_link)
    return audio_elements
