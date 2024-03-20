import requests
import random

def main(url='http://127.0.0.1:5001/'):
    files = {
        'data': open('data.csv', 'rb')
    }
    resp = requests.post(url + 'transactions', files=files)
    assert resp.ok, resp.text

    resp_json = resp.json()
    counter = resp_json['counter']
    hash_certificate = resp_json['password']
    resp = requests.get(f'{url}report?id={counter}&password={tamper(hash_certificate)}')
    assert not resp.ok, resp.text

    resp = requests.get(f'{url}report?id={counter}&password={hash_certificate}')
    assert resp.ok, resp.text

    resp_json = resp.json()
    gross_revenue = resp_json['gross-revenue']
    expenses = resp_json['expenses']
    net_revenue = resp_json['net-revenue']
    assert gross_revenue - expenses == net_revenue

    print('passed!')

def tamper(s):
    idx = random.randint(0, len(s) - 1)
    val = chr(random.randint(ord('A'), ord('z')))
    return s[:idx - 1] + val + s[idx + 1:]

if __name__ == '__main__':
    main()
