from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from azure.cosmos import CosmosClient
import json
import os


endpoint = "https://ml2499-db.documents.azure.com:443/"
key = "eENzBybN77GqV9gVlPsb9IfmiKTHJIX9q4zMF7K0Em36T3S2Xr8zAlcsODo6N6XP1808AY3Hto0vGmoKLcjRZw=="
client = CosmosClient(endpoint, credential = key)
database_name = 'Tasks'
container_name = 'Container1'
database_obj  = client.get_database_client(database_name)
container = database_obj.get_container_client(container_name)

app = Flask(__name__)

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    origin = request.form.get('origin')
    dest = request.form.get('dest')
    for item in container.query_items(query='SELECT * FROM Container1 i', enable_cross_partition_query=True):
        print(json.dumps(item, indent=True))
    if origin and dest:
        return render_template('hello.html', origin = origin, dest = dest)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()