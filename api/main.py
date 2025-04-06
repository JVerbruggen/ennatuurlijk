from dotenv import load_dotenv
from flask import Flask, jsonify
from flasgger import Swagger
from azure.data.tables import TableServiceClient
import os

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)

table_storage_connection_string     = os.getenv("AZURE_TABLE_STORAGE_CONNECTION_STRING")
table_storage_table_name            = os.getenv("AZURE_TABLE_STORAGE_TABLE_NAME")

table_service_client    = TableServiceClient.from_connection_string(table_storage_connection_string)
table_client            = table_service_client.get_table_client(table_storage_table_name)

@app.route('/theme_park/<theme_park>', methods=['GET'])
def get_by_theme_park(theme_park):
    """
    Get all waiting times for given theme park
    ---
    parameters:
      - name: theme_park
        in: path
        type: string
        required: true
    responses:
      200:
        description: List of matching entries
        schema:
          type: array
          items:
            type: object
      500:
        description: Server error
    """
    try:
        # Build the filter query
        filter_query = f"PartitionKey eq '{theme_park}'"

        # Query the table
        entities = table_client.query_entities(query_filter=filter_query)

        # Convert entities to list of dicts
        result = [dict(entity) for entity in entities]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
