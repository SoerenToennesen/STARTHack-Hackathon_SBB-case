# pip install flask
# export FLASK_APP=app.py
# export FLASK_ENV=development
# FLASK_APP=app.py
# flask run

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def data():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers