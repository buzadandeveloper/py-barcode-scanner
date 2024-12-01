from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO
import zxing

app = Flask(__name__)

# Enable CORS
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-image', methods=['POST'])
def send_image():
    try:
        # Receive the JSON with the base64 image data
        data = request.json
        base64_image_string = data.get('base64')

        if not base64_image_string:
            raise ValueError("No image data provided")

        # Debug: Print part of the base64 string to check if it's correctly received
        print(f"Received base64 string (first 100 chars): {base64_image_string[:100]}")

        # Decode the base64 string to get the image data
        image_data = base64.b64decode(base64_image_string)
        image = Image.open(BytesIO(image_data))

        # Use ZXing to decode the barcode from the image directly in memory (no file saving)
        reader = zxing.BarCodeReader()
        barcode = reader.decode(BytesIO(image_data))  # Read directly from the in-memory image data

        if barcode:
            decoded_text = barcode.parsed
        else:
            decoded_text = "No barcode found."

        return jsonify({'message': 'Image successfully scanned.', 'decodedText': decoded_text}), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
