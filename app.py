from flask import Flask, render_template, request
import pandas as pd
import requests

app = Flask(__name__)

@app.route('/main', methods=['POST','GET'])
def main():
    url = 'https://data.chhs.ca.gov/api/3/action/datastore_search?resource_id=160d4cd5-148a-408a-b093-01cacc504320&limit=8230'
    req = requests.get(url, verify=False).json()
    data = req['result']['records']
    data = sorted(data, key=lambda x: x['FACILITY_NAME'])
    print(data)
    df = pd.DataFrame(data)

    if request.method == 'POST':
        selected = request.form.get('main')
        print('selected:', selected)
        subset = df.loc[df['OSHPD_ID'] == selected][['FACILITY_NAME','OSHPD_ID']].copy()
        print('subset', subset)
        table = subset.transpose().to_html(header=False, classes=['table', 'table-responsive'])
        return render_template('index.html', data=data, selected=selected, table=table)
    else:
        return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)