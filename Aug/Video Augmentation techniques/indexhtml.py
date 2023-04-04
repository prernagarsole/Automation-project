
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
            <option value="gaussianblur"> Gaussian Blur </option>
            <option value="horizontalflip">Horizontal Flip </option>
            <option value="randomrotate">Random Rotate </option>
            <option value="flip_vertical">Vertical Flip </option>

        </select>
        <br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>


