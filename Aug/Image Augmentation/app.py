



import os
import random
import io
import numpy as np

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageOps
from PIL import ImageFilter

from skimage.util import random_noise

from flask import Flask, render_template, request, redirect, url_for, send_file, make_response

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload():
    image_file = request.files["image"]
    if image_file:
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        augmentations = request.form.getlist("augmentations")
        filenames = []
        for augmentation in augmentations:
            augmented_image = apply_augmentation(augmentation, image, request.form)
            filename = "augmented_" + str(random.randint(1, 100000000)) + ".jpg"
            filepath = os.path.join(app.config['STATIC_FOLDER'], filename)  # Add folder path to filename
            augmented_image.save(filepath)
            filenames.append(filename)
        return render_template("view.html", filenames=filenames)
    else:
        return redirect(url_for("index"))


def apply_augmentation(augmentation, image, form):
    if augmentation == "rotate":
        degree = int(form["degree"])
        return image.rotate(degree)
    elif augmentation == "flip":
        return ImageOps.flip(image)
    # elif augmentation == "crop":
    #     width = image.width
    #     height = image.height
    #     left = int(form["left"])
    #     upper = int(form["upper"])
    #     right = int(form["right"])
    #     lower = int(form["lower"])
    #     return image.crop((left, upper, right, lower))
    elif augmentation == "crop":
        width, height = image.size
        crop_size = min(width, height)
        left = (width - crop_size) / 2
        upper = (height - crop_size) / 2
        right = left + crop_size
        lower = upper + crop_size
        return image.crop((left, upper, right, lower))
    elif augmentation == "brightness":
        factor = float(form["brightness_factor"])
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    elif augmentation == "contrast":
        factor = float(form["contrast_factor"])
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    # elif augmentation == "color":
    #     brightness_factor = float(form["color_brightness_factor"])
    #     contrast_factor = float(form["color_contrast_factor"])
    #     saturation_factor = float(form["saturation_factor"])
    #     hue_factor = float(form["hue_factor"])
    #     image = ImageEnhance.Brightness(image).enhance(brightness_factor)
    #     image = ImageEnhance.Contrast(image).enhance(contrast_factor)
    #     image = ImageEnhance.Color(image).enhance(saturation_factor)
    #     h, s, v = image.convert('HSV').split()
    #     hue_range = int(hue_factor * 180)
    #     hue_transform = ImageEnhance.Color(h).enhance(0)
    #     hue_transform = hue_transform.rotate(random.randint(-hue_range, hue_range))
    #     return Image.merge('HSV', (hue_transform, s, v)).convert('RGB')

    elif augmentation == "color":
        brightness_factor = float(form.get("color_brightness_factor", 1))
        contrast_factor = float(form.get("color_contrast_factor", 1))
        saturation_factor = float(form.get("saturation_factor", 1))
        hue_factor = float(form.get("hue_factor", 1))
        image = ImageEnhance.Brightness(image).enhance(brightness_factor)
        image = ImageEnhance.Contrast(image).enhance(contrast_factor)
        image = ImageEnhance.Color(image).enhance(saturation_factor)
        h, s, v = image.convert('HSV').split()
        hue_range = int(hue_factor * 180)
        hue_transform = ImageEnhance.Color(h).enhance(0)
        hue_transform = hue_transform.rotate(random.randint(-hue_range, hue_range))
        return Image.merge('HSV', (hue_transform, s, v)).convert('RGB')
    elif augmentation == "blur":
        radius = int(form["radius"])
        return image.filter(ImageFilter.GaussianBlur(radius))
    # elif augmentation == "noise":
    #     amount = int(form["amount"])
    #     width, height = image.size
    #     noise = Image.frombytes('L', (width, height), os.urandom(width * height))
    #     noise = noise.point(lambda x: 0 if x < 128 else 255, '1')
    #     if amount > 0:
    #         noise = noise.filter(ImageFilter.GaussianBlur(amount))
    #     noise = noise.convert('RGBA')
    #     image = image.convert('RGBA')  # Convert image to RGBA
    #     return Image.alpha_composite(image, noise).convert('RGB')
    #     #return Image.alpha_composite(image.convert('RGBA'), noise).convert('RGB')


    # elif augmentation == "noise":
    #     amount = int(form["amount"])
    #     width, height = image.size
    #     noise = (255 * np.random.rand(height, width, 3)).astype(np.uint8)
    #     noise = Image.fromarray(noise)
    #     if amount > 0:
    #         noise = noise.filter(ImageFilter.GaussianBlur(amount))
    #     noise = noise.convert('RGBA')
    #     image = image.convert('RGBA')  # Convert image to RGBA
    #     return Image.alpha_composite(image, noise).convert('RGB')

    elif augmentation == "noise":
        amount = int(form["amount"])
        # Convert image to floating-point format with pixel values between 0 and 1
        img_array = np.array(image).astype(np.float32) / 255.0
        # Apply random noise
        img_noisy = random_noise(img_array, var=(amount / 255.0) ** 2)
        # Convert noisy image back to 8-bit format
        img_noisy = (img_noisy * 255.0).astype(np.uint8)
        return Image.fromarray(img_noisy)


@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(app.config['STATIC_FOLDER'], filename)
    response = make_response(send_file(path, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return response


if __name__ == "__main__":
    app.run(debug=True)





