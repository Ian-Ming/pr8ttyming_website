import azure.functions as func
import os
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor_counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    # We move the import INSIDE the function. 
    # This prevents the "Worker failed to index" error that hides your functions!
    try:
        from azure.cosmos import CosmosClient
        
        conn_str = os.environ.get("CosmosDBConnectionString")
        if not conn_str:
            return func.HttpResponse("Setting 'CosmosDBConnectionString' is missing in Portal.", status_code=500)

        client = CosmosClient.from_connection_string(conn_str)
        database = client.get_database_client("AzureResume")
        container = database.get_container_client("Counter")
        
        item = container.read_item(item="1", partition_key="1")
        item["count"] += 1
        container.replace_item(item="1", body=item)
        
        return func.HttpResponse(json.dumps({"count": item["count"]}), mimetype="application/json")
        
    except ImportError:
        return func.HttpResponse("CRITICAL: azure-cosmos is NOT installed on the server.", status_code=500)
    except Exception as e:
        return func.HttpResponse(f"Database Error: {str(e)}", status_code=500)