








index.html-----


<!DOCTYPE html>
<html>
<head>
    <title>Image Augmentation Tool</title>
</head>
<body>
    <h1>Image Augmentation Tool</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*"><br><br>
        <label>Select augmentations to apply:</label><br>
        <input type="checkbox" name="augmentations" value="rotate">Rotate
        <label for="degree">Degree:</label>
        <input type="number" name="degree" min="-360" max="360" value="0"><br><br>
        <input type="checkbox" name="augmentations" value="flip">Flip<br><br>
        <input type="checkbox" name="augmentations" value="crop">Crop
        <label for="left">Left:</label>
        <input type="number" name="left" min="0" value="0">
        <label for="upper">Upper:</label>
        <input type="number" name="upper" min="0" value="0">
        <label for="right">Right:</label>
        <input type="number" name="right" min="0" value="0">
        <label for="lower">Lower:</label>
        <input type="number" name="lower" min="0" value="0"><br><br>
        <input type="checkbox" name="augmentations" value="brightness">Brightness
        <label for="brightness_factor">Factor:</label>
        <input type="number" name="brightness_factor" min="0" max="5" step="0.1" value="1"><br><br>
        <input type="checkbox" name="augmentations" value="contrast">Contrast
        <label for="contrast_factor">Factor:</label>
        <input type="number" name="contrast_factor" min="0" max="5" step="0.1" value="1"><br><br>
        <input type="checkbox" name="augmentations" value="color">Color
        <label for="brightness_factor">Brightness factor:</label>
        <input type="number" name="brightness_factor" min="0" max="5" step="0.1" value="1">
        <label for="contrast_factor">Contrast factor:</label>
        <input type="number" name="contrast_factor" min="0" max="5" step="0.1" value="1">
        <label for="saturation_factor">Saturation factor:</label>
        <input type="number" name="saturation_factor" min="0" max="5" step="0.1" value="1">
        <label for="hue_factor">Hue factor:</label>
        <input type="number" name="hue_factor" min="0" max="1" step="0.01" value="0"><br><br>
        <input type="checkbox" name="augmentations" value="blur">Blur
        <label for="radius">Radius:</label>
        <input type="number" name="radius" min="0" max="10" value="0"><br><br>
        <input type="checkbox" name="augmentations" value="noise">Noise
        <label for="amount">Amount:</label>
        <input type="number" name="amount" min="0" max="100" value="0"><br><br>

        <input type="submit" value="Apply">
    </form>
</body>
</html>


