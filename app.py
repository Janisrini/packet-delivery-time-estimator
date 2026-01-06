from flask import Flask, render_template, request, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    estimated_time = None
    inputs = {}

    if request.method == 'POST':
        try:
            distance = float(request.form['distance']) * 1000
            packet_size = float(request.form['packet']) * 8
            bandwidth = float(request.form['bandwidth']) * 1e6
            delay = float(request.form['delay'])

            propagation_speed = 2e8

            transmission_time = (packet_size / bandwidth) * 1000
            propagation_time = (distance / propagation_speed) * 1000

            estimated_time = round(transmission_time + propagation_time + delay, 2)

            inputs = {
                'distance': request.form['distance'],
                'packet': request.form['packet'],
                'bandwidth': request.form['bandwidth'],
                'delay': request.form['delay'],
                'result': estimated_time
            }

        except ValueError:
            estimated_time = "Invalid input."

    return render_template('index.html', result=estimated_time, inputs=inputs)

@app.route('/download', methods=['POST'])
def download_csv():
    data = request.form
    filename = f"packet_estimation_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = os.path.join("static", filename)

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Distance (km)", "Packet Size (bytes)", "Bandwidth (Mbps)", "Delay (ms)", "Estimated Time (ms)"])
        writer.writerow([data['distance'], data['packet'], data['bandwidth'], data['delay'], data['result']])

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)