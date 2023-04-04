from flask import Flask, request, jsonify
import librosa
import soundfile as sf
from audiomentations import Compose, AddGaussianNoise, PitchShift, HighPassFilter, TimeStretch, AddBackgroundNoise, PolarityInversion, Clip, GainTransition, Trim, Mp3Compression, LoudnessNormalization, RoomSimulator
import numpy as np

app = Flask(__name__)

augmentation_profiles = {
    "Add Gaussian Noise Augmentation": Compose(
        [
            AddGaussianNoise(min_amplitude=0.01, max_amplitude=0.015, p=1),
            PitchShift(min_semitones=-8, max_semitones=8, p=1),
            HighPassFilter(min_cutoff_freq=2000, max_cutoff_freq=4000, p=1)
        ]
    ),
    "High PassFilter Augmentation": Compose(
        [
            HighPassFilter(min_cutoff_freq=1000, max_cutoff_freq=3000, p=1)
        ]
    ),
    "Time Stretch Augmentation": Compose(
        [

            TimeStretch(min_rate=0.8, max_rate=1.2, p=1)
        ]
    ),
    "Add Background Noise Augmentation": Compose(
        [

            AddBackgroundNoise(sounds_path="/Users/spartan/PycharmProjects/aaaa/venv", min_snr_in_db=3.0,
                               max_snr_in_db=30.0, noise_transform=PolarityInversion(), p=1.0)
        ]
    ),
    "Clip Augmentation": Compose(
        [
            Clip(a_min=-4.0, a_max=8.0, p=0.5)
        ]
    ),
    "Gain Transition Augmentation": Compose(
        [
            GainTransition(min_gain_in_db=0.1, max_gain_in_db=10.0, max_duration=5)
        ]
    ),
    "Trim Augmentation": Compose(
        [
            Trim(top_db=100.0)
        ]
    ),
    "Mp3 Compression Augmentation": Compose(
        [
            Mp3Compression(min_bitrate=32, max_bitrate=220, backend="pydub", p=1.0)

        ]
    ),
    "Loudness Normalization Augmentation": Compose(
        [
            LoudnessNormalization(min_lufs_in_db=-40, max_lufs_in_db=-40, p=1.0)

        ]
    ),
    "RoomSimulator Augmentation": Compose(
        [
            RoomSimulator(min_size_x=3.6, max_size_y=10.6,min_absorption_value=1.0, p=1)

        ]
    ),
    "Pitch Shift Augmentation": Compose(
        [
            PitchShift(min_semitones=-8, max_semitones=8, p=1)

        ]
    ),
    "High Pass Filter Augmentation": Compose(
        [

            HighPassFilter(min_cutoff_freq=2000, max_cutoff_freq=4000, p=1)
        ]
    )
}


@app.route("/")
def index():
    return """
        <html>
            <body>
                <form action="/augment_audio" method="post" enctype="multipart/form-data">
                    <input type="file" name="audio_file">
                    <select name="augmentation_profile">
                        {}
                    </select>
                    <input type="submit" value="Augment Audio">
                </form>
            </body>
        </html>
    """.format("\n".join(f"<option value='{p}'>{p}</option>" for p in augmentation_profiles.keys()))


@app.route("/augment_audio", methods=["GET", "POST"])
def augment_audio():
    if request.method == "POST":
        # Get audio file from the request
        audio_file = request.files.get("audio_file")
        if audio_file is None:
            return jsonify({"error": "Audio file not found in the request"}), 400

        # Get the selected augmentation profile from the request
        augmentation_profile = request.form.get("augmentation_profile")
        if augmentation_profile is None:
            return jsonify({"error": "Augmentation profile not selected"}), 400

        # Load the audio file
        signal, sr = librosa.load(audio_file, sr=None)

        # Augment the audio
        augment_raw_audio = augmentation_profiles.get(augmentation_profile)
        if augment_raw_audio is None:
            return jsonify({"error": f"Augmentation profile '{augmentation_profile}' not found"}), 400
        augmented_signal = augment_raw_audio(signal, sr)

        # Save the augmented audio as a .wav file
        sf.write("augmented_audio.wav", augmented_signal, sr)

        return jsonify({"message": "Audio augmentation successful"})

    return """
        <html>
            <body>
                <form action="/augment_audio" method="post" enctype="multipart/form-data">
                    <input type="file" name="audio_file">
                    <select name="augmentation_profile">
                        <option value="volume_augmentation">Volume Augmentation</option>
                        <option value="pitch_augmentation">Pitch Augmentation</option>
                        <option value="noise_augmentation">Noise Augmentation</option>
                        <option value="stretch_augmentation">Stretch Augmentation</option>
                    </select>
                    <input type="submit" value="Augment Audio">
                </form>
            </body>
        </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
