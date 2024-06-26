import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import numpy as np
import pandas as pd
from pred import predict_instance
from mailer import send_malicious_ip_alert
app = Flask(__name__)

host = 'localhost'
db_user = 'root'
db_password = 'root'
database = 'nids'
port = '3306'

def process_excel_data():
    connection = mysql.connector.connect(
        host=host,
        user=db_user,
        password=db_password,
        database=database,
        port=port
    )

    file_path = "static/excel/"
    file = file_path + os.listdir(file_path)[0]

    df = pd.read_excel(file)
    df.drop(columns='Timestamp', inplace=True)

    cursor = connection.cursor()

    for index, row in df.iterrows():
        ip_address = row['IP Address']
        test_scenario = row['Test Scenario']    
        test_scenario = re.sub(r"\s+", "", test_scenario)
        new_instance = [float(value) for value in test_scenario.split(",")]
        label = predict_instance(new_instance)
        print("Test Scenario:", test_scenario)
        check_query = f"SELECT * FROM Test_Scenario WHERE IP_Address = '{ip_address}'"
        cursor.execute(check_query)
        existing_record = cursor.fetchone()

        if existing_record:
            print(f"Record with IP address {ip_address} already exists.")
        else:
            insert_query = f"""
            INSERT INTO Test_Scenario (IP_Address, Test_Scenario, Label) 
            VALUES ('{ip_address}', '{test_scenario}', '{label}')
            """
            cursor.execute(insert_query)
    
    connection.commit()
    connection.close()




UPLOAD_FOLDER = 'static/excel'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', message='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', message='No selected file')
        if file:
            existing_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'google_form_responses.xlsx')
            if os.path.exists(existing_file_path):
                os.remove(existing_file_path)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'google_form_responses.xlsx'))
            process_excel_data()
            return redirect(url_for('home')) 
    return render_template('upload.html')




@app.route('/')
def nids():
    return render_template('NIDS.html')


@app.route('/home')
def home():
    connection = mysql.connector.connect(
        host=host,
        user=db_user,
        password=db_password,
        database=database,
        port=port
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Test_Scenario")
    data = cursor.fetchall()

    for entry in data:
        test_scenario = entry['Test_Scenario']
        lines = test_scenario.split('\n')
        entry['Test_Scenario'] = '<br>'.join(lines)
        
    connection.close()
    send_malicious_ip_alert(data,['nagendrakashyap8055@gmail.com','manishmithilesh42@gmail.com'])
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)
