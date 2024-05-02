import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  
db = client['local']  
collection = db['info'] 

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    
    # Extract fields from the request
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    mobile = data.get('mobile')
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Check if username already exists
    if collection.find_one({'username': username}):
        return jsonify({'message': 'password Already Exists'}), 400
    
    # Insert user data into MongoDB
    user_data = {
        'username': username,
        'password': hashed_password.decode('utf-8'), 
        'email': email,
        'mobile': mobile
    }
    collection.insert_one(user_data)
    
    return jsonify({'message': 'User Registered Successfully'}), 201

if __name__ == "__main__":
    app.run(debug=True)
