import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor_counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Use .get() to prevent a crash if the variable is missing
        conn_str = os.environ.get("CosmosDBConnectionString")
        
        if not conn_str:
            return func.HttpResponse("Error: CosmosDBConnectionString is missing in Portal.", status_code=500)

        client = CosmosClient.from_connection_string(conn_str)
        database = client.get_database_client("AzureResume")
        container = database.get_container_client("Counter")
        
        # Point read for id="1"
        item = container.read_item(item="1", partition_key="1")
        item["count"] += 1
        container.replace_item(item="1", body=item)
        
        return func.HttpResponse(
            json.dumps({"count": item["count"]}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        # If it crashes here, you'll see why in your browser!
        return func.HttpResponse(f"Database Error: {str(e)}", status_code=500)