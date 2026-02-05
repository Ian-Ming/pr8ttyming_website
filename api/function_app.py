import azure.functions as func
import json
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitor_counter")
def visitor_counter(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Move the import here!
        from azure.cosmos import CosmosClient 
        
        conn_str = os.environ.get("CosmosDBConnectionString")
        client = CosmosClient.from_connection_string(conn_str)
        # ... rest of your code ...
        return func.HttpResponse("Success!", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Import or Logic Error: {str(e)}", status_code=500)