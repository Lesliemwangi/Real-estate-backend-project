from flask import Flask, jsonify
from flask_cors import CORS
from resources.properties import scrape_properties  # Importing the scrape_properties function

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests
# Define a route for the root URL
@app.route('/')
def home():
    return 'Welcome to the Property Scraper API!'

# Define a route to return scraped property data
@app.route('/properties', methods=['GET'])
def get_properties():
    properties = scrape_properties()
    if properties:
        return jsonify(properties)
    else:
        return jsonify({'error': 'Failed to retrieve property data'}), 500

if __name__ == '__main__':
    app.run(debug=True)

