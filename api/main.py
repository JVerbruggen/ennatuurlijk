from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify
from flasgger import Swagger

from ridestore import *
from waitingtime_logic import *

app = Flask(__name__)
swagger = Swagger(app, template={
    "info": {
        "title": "Theme Park Waiting Times API (TPWT)",
        "description": "Theme Park Waiting Times API (TPWT) is an easy to use and free API to get up-to-date and historic waiting time data.",
        "version": "1.0.0",
        "contact": {
            "name": "Jurjen V."
        }
    }
})


waiting_time_logic = WaitingTimeLogic()

@app.route('/theme_parks/', methods=['GET'])
def get_theme_parks():
    """
    Get all available theme parks
    ---
    tags:
        - Available Parks and Rides
    responses:
      200:
        description: List of available theme parks
        schema:
          type: array
          items:
            type: object
      500:
        description: Server error
    """
    try:
        ride_store = RideStore()

        return jsonify(ride_store.get_known_theme_parks()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ride_names/<theme_park>/', methods=['GET'])
def get_ride_names(theme_park):
    """
    Get all available ride names
    ---
    tags:
        - Available Parks and Rides
    parameters:
      - name: theme_park
        in: path
        type: string
        required: true
    responses:
      200:
        description: List of available ride names
        schema:
          type: array
          items:
            type: object
      500:
        description: Server error
    """
    try:
        ride_store = RideStore()
        assert ride_store.validate_theme_park(theme_park), "Unknown theme park"

        return jsonify(ride_store.get_known_rides(theme_park)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/daily/<theme_park>/<ride_name>', methods=['GET'])
def get_daily(theme_park, ride_name):
    """
    Get the todays waiting times for a ride, grouped per hour
    ---
    tags:
        - Waiting Time Data
    parameters:
      - name: theme_park
        in: path
        type: string
        required: true
      - name: ride_name
        in: path
        type: string
        required: true
    responses:
      200:
        description: List of waiting averages
        schema:
          type: array
          items:
            type: object
      500:
        description: Server error
    """
    try:
        ride_store = RideStore()
        assert ride_store.validate_theme_park(theme_park), "Unknown theme park"
        assert ride_store.validate_ride_name(theme_park, ride_name), "Unknown ride"

        result = waiting_time_logic.get_hourly_waiting_times(theme_park, ride_name)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/daily_averages/<theme_park>/<ride_name>', methods=['GET'])
def get_daily_averages(theme_park, ride_name):
    """
    Get the todays waiting averages for a ride, grouped per hour
    ---
    tags:
        - Waiting Time Data
    parameters:
      - name: theme_park
        in: path
        type: string
        required: true
      - name: ride_name
        in: path
        type: string
        required: true
    responses:
      200:
        description: List of waiting averages
        schema:
          type: array
          items:
            type: object
      500:
        description: Server error
    """
    try:
        ride_store = RideStore()
        assert ride_store.validate_theme_park(theme_park), "Unknown theme park"
        assert ride_store.validate_ride_name(theme_park, ride_name), "Unknown ride"

        result = waiting_time_logic.get_hourly_waiting_time_averages(theme_park, ride_name)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    load_dotenv()

    if os.getenv("DEBUG_MODE") == "TRUE":
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=5000)
