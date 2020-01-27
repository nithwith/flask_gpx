# Observatory Service

# Import framework
from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api
import json
import uuid
from flask_swagger_ui import get_swaggerui_blueprint

# Instantiate the app
app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "flask_gpx"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

api = Api(app)

# Work with Json file

def get_rides_on_json():
    with open('maps.json') as json_file:
        data = json.load(json_file)
    return data

def add_ride_on_json(new_title, new_data):
    with open("maps.json", 'r') as f:
        data = json.loads(f.read())
    data[new_title] = new_data
    with open("maps.json", 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

# REST API


@app.route('/rides', methods=['GET'])
def get_rides():
    rides_json = get_rides_on_json()
    return jsonify({'rides': rides_json})


@app.route('/ride/<string:ride_id>', methods=['GET'])
def get_ride(ride_id):
    rides_json = get_rides_on_json()
    ride = []
    for key in rides_json.keys():
        if rides_json[key]['id'] == ride_id:
            ride = rides_json[key]
            break
    if len(ride) == 0:
        abort(404)
    return jsonify({'ride': ride})

@app.route('/rides', methods=['POST'])
def create_ride():
    if not request.json or not 'title' in request.json:
        abort(400)
    new_id = str(uuid.uuid1())
    new_ride = {
        'id': new_id,
        'title': request.json.get('title', ""),
        'type': request.json.get('type', "")}

    add_ride_on_json(request.json.get('title', ""), new_ride)
    return get_ride(new_id)


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)



