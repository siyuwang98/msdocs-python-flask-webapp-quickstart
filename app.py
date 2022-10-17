from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from azure.cosmos import CosmosClient
import json
import os


endpoint = os.environ.get('COSMOS_ENDPOINT')
key = os.environ.get('COSMOS_KEY')
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

@app.route('/results', methods=['POST'])
def results():
    origin = request.form.get('origin').strip()
    dest = request.form.get('dest').strip()
    if origin != "Ithaca":
        return render_template('error.html', errorMsg = "Origin Not Supported")
    if dest != "NYC":
        return render_template('error.html', errorMsg = "Destination Not Supported")

    count = 1
    ret = []
    for stop1 in container.query_items(query="SELECT * FROM Container1 i WHERE i.origin='{}'".format(origin), enable_cross_partition_query=True):
        print(stop1)
        for stop2 in container.query_items(query="SELECT * FROM Container1 i WHERE i.origin='{}' AND i.destination='{}'".
            format(stop1["destination"], dest), enable_cross_partition_query=True):
            for p1 in stop1["options"]:
                for p2 in stop2["options"]:
                    ret.append({"id": count, "price": p1["price"] + p2["price"], "stops": "{}, {}, {}".format(origin, stop1["destination"], dest)})
                    count += 1

    if len(ret):
        return render_template('results.html', origin = origin, dest = dest, data = ret)
    else:
        return render_template('error.html', errorMsg = "Results not Found")

if __name__ == '__main__':
   app.run()