# Create a base Flask server

import pickle
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable CORS with restricted origins (not wildcard)
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')

@app.after_request
def after_request(response):
    """
    Enable CORS with restricted origins
    """
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


# Load model from pickle file securely
# WARNING: Only load pickle files from trusted sources
model = pickle.load(open('model.pkl', 'rb'))

# Model takes two parameters - day of week and airport id, then returns a prediction of flight delay
@app.route('/predict', methods=['GET'])
def predict():
    """
    Takes two parameters - day of week and airport id, then returns a prediction of flight delay
    """
    try:
        # Validate and store day_of_week as int (0-6 for days of week)
        day_of_week_str = request.args.get('day_of_week')
        airport_id_str = request.args.get('airport_id')
        
        if not day_of_week_str or not airport_id_str:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        day_of_week = int(day_of_week_str)
        airport_id = int(airport_id_str)
        
        # Validate ranges
        if not (0 <= day_of_week <= 6):
            return jsonify({'error': 'day_of_week must be between 0 and 6'}), 400
        if airport_id < 0:
            return jsonify({'error': 'airport_id must be non-negative'}), 400
        
        prediction = model.predict_proba([[day_of_week, airport_id]])[0]
        
        # Split prediction string by space
        prediction = str(prediction).split(' ')

        # store first value from prediction as certainty, and remove the first character
        certainty = float(prediction[0][2:])

        # store second value from prediction as delay, and remove the last character
        delay = float(prediction[1][:-1])

        # return prediction as json
        return jsonify({'certainty': certainty, 'delay': delay})
    except (ValueError, IndexError) as e:
        return jsonify({'error': 'Invalid input parameters'}), 400
    except Exception as e:
        app.logger.error(f'Prediction error: {str(e)}')
        return jsonify({'error': 'Prediction failed'}), 500

# Create a new route called airports with method of get
@app.route('/airports', methods=['GET'])
def airports():
    try:
        # Load airports from csv file
        with open('airports.csv', 'r') as f:
            airports = f.readlines()

        # Remove first line of airports
        airports.pop(0)

        # Create list with dictionary of airports
        # First value is id, second is name
        # Convert id to integer
        # Remove last character from name
        airports = [{'id': int(airport.split(',')[0]), 'name': airport.split(',')[1][:-1]} for airport in airports]
        # Sort by name
        airports = sorted(airports, key=lambda k: k['name'])

        return jsonify(airports)
    except FileNotFoundError:
        return jsonify({'error': 'Airports data file not found'}), 404
    except Exception as e:
        app.logger.error(f'Error loading airports: {str(e)}')
        return jsonify({'error': 'Failed to load airports'}), 500

if __name__ == '__main__':
    # Disable debug mode and use environment-based config
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug)