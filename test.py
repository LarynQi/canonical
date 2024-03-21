import requests
import random
import sys

def main(url='http://127.0.0.1:5001/'):
    files = {
        'data': open('data.csv', 'rb')
    }
    resp = requests.post(url + 'transactions', files=files)
    assert resp.ok, resp.text

    resp_json = resp.json()
    counter = resp_json['id']
    key = resp_json['key']
    resp = requests.get(f'{url}report?id={counter}&key={tamper(key)}')
    assert not resp.ok, resp.text
    
    resp = requests.get(f'{url}report?id=-1&key={key}')
    assert not resp.ok, resp.text

    resp = requests.get(f'{url}report?id={counter}&key={key}')
    assert resp.ok, resp.text

    resp_json = resp.json()
    gross_revenue = resp_json['gross-revenue']
    expenses = resp_json['expenses']
    net_revenue = resp_json['net-revenue']
    assert gross_revenue - expenses == net_revenue

    print('test passed!')

def tamper(s):
    idx = random.randint(0, len(s) - 1)
    val = chr(random.randint(ord('A'), ord('z')))
    return s[:idx - 1] + val + s[idx + 1:]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(url=sys.argv[1])
    else:
        main()
