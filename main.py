from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Importă CORS
import base64
from PIL import Image
from io import BytesIO
import zxing

app = Flask(__name__, template_folder='barcodeScanner/templates')

# Activează CORS pentru toate rutele
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-image', methods=['POST'])
def send_image():
    try:
        data = request.json
        base64_image_string = data.get('base64')

        if not base64_image_string:
            raise ValueError("No image data provided")

        image_data = base64.b64decode(base64_image_string)
        image = Image.open(BytesIO(image_data))

        # Salvează imaginea
        image_path = "decoded_image.jpg"
        image.save(image_path)

        # Scanează imaginea pentru datele codului de bare
        reader = zxing.BarCodeReader()
        barcode = reader.decode(image_path)
        if barcode:
            decoded_text = barcode.parsed
        else:
            decoded_text = "No barcode found."

        return jsonify({'message': 'Image successfully scanned.', 'decodedText': decoded_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
