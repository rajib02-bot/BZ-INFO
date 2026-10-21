from flask import Flask, request, jsonify

app = Flask(__name__)

# ============================================
# API KEY CONFIGURATION (Apni Marzi Ki Key)
# ============================================
MY_SECRET_API_KEY = "bazigar_secret_12345"

# ============================================
# YOUR DATABASE (Mock Data)
# ============================================
DATABASE = {
    "9876543210": {
        "num": "+91 9876543210",
        "name": "Rahul Sharma",
        "fname": "Suresh Sharma",
        "aadhar": "[Aadhaar Redacted]",
        "address": "New Delhi, Delhi, India",
        "circle": "Delhi NCR",
        "alt": "9811122233",
        "email": "rahul.sharma@example.com"
    },
    "9123456789": {
        "num": "+91 9123456789",
        "name": "Amit Kumar",
        "fname": "Rajesh Kumar",
        "aadhar": "[Aadhaar Redacted]",
        "address": "Kolkata, West Bengal, India",
        "circle": "West Bengal",
        "alt": "",
        "email": "amit@example.com"
    }
}

# ============================================
# API LOOKUP ROUTE
# ============================================
@app.route('/api/v1/lookup', methods=['GET'])
def lookup():
    user_key = request.args.get('key')
    number = request.args.get('num')

    # 1. API Key Check
    if not user_key or user_key != MY_SECRET_API_KEY:
        return jsonify({
            "status": "error",
            "message": "Invalid or missing API Key"
        }), 401

    # 2. Number Check
    if not number:
        return jsonify({
            "status": "error",
            "message": "Phone number is required"
        }), 400

    # 3. Fetch Data
    if number in DATABASE:
        return jsonify({
            "status": "success",
            "result": [DATABASE[number]],
            "BUY_API": "t.me/hckr_BaziGarr",
            "SUPPORT": "t.me/hckr_BaziGarr"
        })
    else:
        return jsonify({
            "status": "error",
            "message": "No records found for this number"
        }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
