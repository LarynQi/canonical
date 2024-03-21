from flask import Flask, request, make_response, jsonify
import pandas as pd
import csv
import os
import sys
import hashlib

app = Flask(__name__)
app.config['FILE_UPLOADS'] = sys.path[0] + '/db/'

refresh_counter = lambda: max(map(lambda filename: int(filename.split('.')[0]), filter(lambda filename: filename[-4:] == '.csv', os.listdir(app.config['FILE_UPLOADS']) + ['-1.csv']))) + 1
    
counter = refresh_counter()

COLUMNS = ['Date', 'Type', 'Amount($)', 'Memo']

@app.route('/transactions', methods=['POST'])
def transactions():
    global counter
    counter = refresh_counter()
    data = []
    if request.files:
        uploaded_file = request.files['data']
        filepath = os.path.join(app.config['FILE_UPLOADS'], f'{counter}.csv')
        uploaded_file.save(filepath)
        with open(filepath, 'r') as f:
            csv_file = csv.reader(f)
            for row in csv_file:
                if not row or row[0].strip()[0] == '#':
                    continue
                data.append(map(lambda val: val.strip(), row))
        with open(filepath, 'w') as f:
            f.write(','.join(COLUMNS) + '\n')
            for row in data:
                f.write('"' + '","'.join(row) + '"\n')
    counter += 1
    m = hashlib.sha512()
    m.update(open(filepath).read().encode('utf-8'))
    hash_certificate = m.hexdigest()
    return make_response(
        jsonify({
            'id': counter - 1,
            'key': hash_certificate
        }),
        200
    )
    return counter - 1

@app.route('/report', methods=['GET'])
def report():
    identifier = request.args.get('id')
    if identifier is None:
        return make_response(
            "Dataset ID was not provided.",
            400
        )
    filepath = app.config['FILE_UPLOADS'] + identifier + '.csv'
    if not os.path.isfile(filepath):
        return make_response(
            "Requested dataset ID does not exist.",
            400
        )
    hash_certificate = request.args.get('key')
    if hash_certificate is None:
        return make_response(
            "Key was not provided.",
            400
        )
    m = hashlib.sha512()
    m.update(open(filepath).read().encode('utf-8'))
    hash_verification = m.hexdigest()
    if hash_certificate != hash_verification:
        return make_response(
            "Wrong key.",
            400
        )
    df = pd.read_csv(filepath)
    gross_revenue = df[df['Type'] == 'Income']['Amount($)'].sum()
    expenses = df[df['Type'] == 'Expense']['Amount($)'].sum()
    net_revenue = gross_revenue - expenses
    return make_response(
        jsonify({
            'gross-revenue': gross_revenue,
            'expenses': expenses,
            'net-revenue': net_revenue
        }),
        200
    )
    
@app.route('/', methods=['GET'])
def home():
    return f'canonical server by Laryn Qi. last updated 3/20/24.'

if __name__ == '__main__':
    app.run(port=5001)
