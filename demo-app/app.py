from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(os.getenv('SERVICE_NAME'))

@app.route('/call/<service_name>')
def call_service(service_name):
    result = requests.get(
        'http://' + str(service_name) + ':8080/',
        headers={"Authorization": request.headers.get('Authorization', ''),}
    )
    return jsonify(str(service_name) + " says: " + str(result.text))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
