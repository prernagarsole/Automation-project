
<!DOCTYPE html>
<html>
<head>
    <title>Augmented Images</title>
    <style>
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            grid-gap: 20px;
        }
        .grid-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 1px solid #ddd;
            padding: 10px;
            margin: 10px;
        }
        .grid-item img {
            max-width: 100%;
            height: auto;
            margin-bottom: 10px;
        }
        .grid-item button {
            padding: 5px 10px;
            background-color: #4CAF50;
            border: none;
            color: white;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin-top: 10px;
            cursor: pointer;
        }
        .grid-item button:hover {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>
    <h1>Augmented Images</h1>
    {% if filenames %}
        <div class="grid-container">
            {% for filename in filenames %}
                <div class="grid-item">
                    <a href="{{ url_for('static', filename=filename) }}" download="{{ filename }}"><img src="{{ url_for('static', filename=filename) }}" alt="{{ filename }}"></a>
                    <button onclick="window.location.href='{{ url_for('download', filename=filename) }}'">Download {{ filename }}</button>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p>No augmentations selected.</p>
    {% endif %}
    <p><a href="{{ url_for('index') }}">Upload another image</a></p>
</body>
</html>
