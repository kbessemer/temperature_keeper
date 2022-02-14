from flask import jsonify, request, render_template, flash, redirect, url_for
from database_driver import app, db, Users, Temperature
from funcfile import query_by_name, query_by_rfid, query_by_barcode, csv_analyze, db_list, delete_user_entry, delete_temp_entry, add_new_user, edit_user_entry, view_profile, temp_write, get_temps, temp_14_days, query_search, highest_temp, lowest_temp, avg_temp, edit_temp_entry
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/get_db')
def get_db():
    response_object = {'Success':True}
    response_object['users'] = db_list()
    return jsonify(response_object)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'Success': False, 'Errors': "Error Code 105 - No file found"})
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return jsonify({'Success': False, 'Errors': "Error Code 106 - Empty File Name"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(csv_analyze(os.path.abspath(f'{os.getcwd()}/uploads/{filename}')))
        else:
            return jsonify({'Success': False, 'Errors': "Error Code 108 - Unallowed file extension"})

@app.route('/search', methods=["POST"])
def search():
    if request.method == 'POST':
        value = request.json['value']
        return jsonify(query_search(value))

@app.route('/delete_user', methods=["POST"])
def delete_user():
    if request.method == 'POST':
        id = request.json['id']
        return jsonify(delete_user_entry(id))

@app.route('/delete_temp', methods=["POST"])
def delete_temp():
    if request.method == 'POST':
        id = request.json['id']
        return jsonify(delete_temp_entry(id))

@app.route('/add_user', methods=["POST"])
def add_user():
    if request.method == 'POST':
        user_name = request.json['name']
        user_rfid = request.json['rfid']
        user_barcode = request.json['barcode']
        return jsonify(add_new_user(user_name, user_rfid, user_barcode))

@app.route('/edit_user', methods=["POST"])
def edit_user():
    if request.method == 'POST':
        id = request.json['id']
        user_name = request.json['name']
        user_rfid = request.json['rfid']
        user_barcode = request.json['barcode']
        return jsonify(edit_user_entry(id, user_name, user_rfid, user_barcode))

@app.route('/edit_temp', methods=["POST"])
def edit_temp():
    if request.method == 'POST':
        id = request.json['id']
        temp = request.json['temp']
        return jsonify(edit_temp_entry(id, temp))

@app.route('/profile_data/<user_id>', methods=["GET"])
def profile_data(user_id):
    return jsonify(view_profile(user_id))

@app.route('/add_temp', methods=["POST"])
def add_temp():
    if request.method == 'POST':
        owner = request.json['id']
        temp = request.json['temp']
        return jsonify(temp_write(owner, temp))

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)