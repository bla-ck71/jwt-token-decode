from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({
        "message": "JWT Decoder API",
        "endpoints": {
            "decode": "POST /decode - Decode a JWT token",
            "health": "GET /health - Check API status"
        }
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "JWT Decoder API"})

@app.route('/decode', methods=['POST', 'GET'])
def decode_jwt():
    # Get token from request
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'token' not in data:
            return jsonify({"success": False, "error": "Token is required"}), 400
        token = data['token'].strip()
    else:  # GET request
        token = request.args.get('token', '').strip()
        if not token:
            return jsonify({"success": False, "error": "Token is required"}), 400
    
    # Check if the token looks like a JWT (three parts separated by dots)
    if len(token.split('.')) != 3:
        return jsonify({
            "success": False, 
            "error": "Invalid JWT format. Token should have three parts separated by dots."
        }), 400
    
    try:
        # Decode the token without verifying the signature
        decoded_data = jwt.decode(token, options={"verify_signature": False})
        return jsonify({"success": True, "decoded": decoded_data})
    
    except jwt.DecodeError:
        return jsonify({"success": False, "error": "Invalid token! Unable to decode."}), 400
    
    except Exception as e:
        return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)