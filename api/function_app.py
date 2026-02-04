import azure.functions as func
import json
import os
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor_counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    # 1. Get the connection string from environment variables
    conn_str = os.environ["CosmosDBConnectionString"]
    client = CosmosClient.from_connection_string(conn_str)
    
    # 2. Connect to the database and container
    database = client.get_database_client("AzureResume")
    container = database.get_container_client("Counter")
    
    # 3. Read the item (id="1"), increment it, and update it
    item = container.read_item(item="1", partition_key="1")
    item["count"] += 1
    container.replace_item(item="1", body=item)
    
    # 4. Return the new count
    return func.HttpResponse(
        json.dumps({"count": item["count"]}),
        mimetype="application/json",
        status_code=200
    )