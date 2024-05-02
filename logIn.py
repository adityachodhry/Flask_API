import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  
db = client['local']  
collection = db['info'] 

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    
    # Extract username and password from the request
    username = data.get('username')
    password = data.get('password')
    
    # Retrieve user document from the database based on username
    user_data = collection.find_one({'username': username})
    if user_data:
        # Retrieve hashed password from the user document
        hashed_password = user_data['password']
        
        # Check if the provided password matches the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return jsonify({'message': 'Login successful'}), 200
        else:
            # Check if username is same but password is different
            existing_user_password = user_data['password']
            if password != existing_user_password:
                return jsonify({'message': 'Login successful (Different Password)'}), 200
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
