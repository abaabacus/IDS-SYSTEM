import csv
import os
import re
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
from pred import predict_instance
from mailer import send_malicious_ip_alert

app = Flask(__name__)

UPLOAD_FOLDER = 'static/excel'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_excel_data():
    file_path = "static/excel/"
    file = file_path + os.listdir(file_path)[0]

    df = pd.read_excel(file)
    # df.drop(columns='Timestamp', inplace=True)    

    with open('test_scenarios.csv', 'w', newline='') as csvfile:
        fieldnames = ['IP_Address', 'Test_Scenario', 'Label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for index, row in df.iterrows():
            ip_address = row['IP Address']
            test_scenario = row['Test Scenario']
            test_scenario = re.sub(r"\s+", "", test_scenario)
            new_instance = [float(value) for value in test_scenario.split(",")]
            label = predict_instance(new_instance)
            writer.writerow({'IP_Address': ip_address, 'Test_Scenario': test_scenario, 'Label': label})

    print("CSV file 'test_scenarios.csv' has been created with the test scenarios.")

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
@app.route('/gettest')
def getttest():
    return render_template('gettestdata.html')


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        ip_address = request.form.get('ipAddress')
        test_data = request.form.get('testData')
        
        print(ip_address)
        test_data = re.sub(r"\s+", "", test_data)
        test_data = [float(value) for value in test_data.split(",")]

        print(test_data)
        prediction=predict_instance(test_data)
        print(prediction)
        data = {'IP_Address':ip_address ,
        'test_data': test_data,
        'Label': prediction}
        data = pd.DataFrame(data)
        send_malicious_ip_alert(data,['avaishnavi644@gmail.com','ananyamahadev19@gmail.com','ananya19032002@gmail.com'])

        return render_template('result.html', ipAddress=ip_address, testData=test_data, prediction=prediction)
@app.route('/')
def nids():
    return render_template('NIDS.html')

@app.route('/home')
def home():
    data = []
    with open('test_scenarios.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_scenario = row['Test_Scenario']
            lines = test_scenario.split('\n')
            row['Test_Scenario'] = '<br>'.join(lines)
            data.append(row)
    
    send_malicious_ip_alert(data, ['ananyamahadev19@gmail.com'])
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
