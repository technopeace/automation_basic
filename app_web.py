# app_web.py
from flask import Flask, render_template, request, jsonify
import logging
from core_logic import process_user_data  # <-- IMPORT the shared logic

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
    """
    Gets data from the web request, passes it to the core logic,
    and returns the result as JSON.
    """
    data = request.json
    name = data.get('name')
    age = data.get('age')
    
    # Call the shared logic function
    result_message = process_user_data(name, age)
    
    if result_message:
        # If logic was successful, return the message
        # Also print to console for the CI test to see
        print(result_message.replace("\n", " "))
        return jsonify({"message": result_message})
    else:
        # If logic returned an error, return an error response
        return jsonify({"error": "Please fill in all fields!"}), 400

if __name__ == '__main__':
    # Runs the web server on the default port for Electron to load
    app.run(port=5000)
