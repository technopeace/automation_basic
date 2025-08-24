# app_web.py
from flask import Flask, render_template, request, jsonify
import logging

# Reduce console noise from the web server for cleaner test logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_data():
    """Receives data from the form and returns a success message."""
    data = request.json
    name = data.get('name')
    age = data.get('age')
    
    if name and age:
        # This print statement is what the CI test will look for
        print(f"Saved! Name: {name} Age: {age}")
        return jsonify({"message": f"Saved!\nName: {name}\nAge: {age}"})
    
    return jsonify({"error": "Please fill in all fields!"}), 400

if __name__ == '__main__':
    # Runs the web server on the default port for Electron to load
    app.run(port=5000)