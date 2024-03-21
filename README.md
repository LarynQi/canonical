# canonical
Laryn Qi

*there is a publicly available deployment of this project here: https://www.ocf.berkeley.edu/~lqi/canonical/

**git repo: https://github.com/LarynQi/canonical

***developed, tested, and deployed on Python 3.9

## environment setup

```shell
python3 -m venv env && source env/bin/activate
pip install -r requirements.txt
python3 setup.py
```

## testing

### local/development

in one shell,
```shell
python3 app.py
```

in another shell,
```shell
python3 test.py
```

### production

```shell
python3 test.py {PATH_TO_SERVER}
```

e.g.
```shell
python3 test.py https://www.ocf.berkeley.edu/~lqi/canonical/
```

## API

### `POST /transactions`
Takes as input a CSV file and returns an `id` and `key` to be used for a request to `/report`.

The CSV file should have column values `Date, Type, Amount($), Memo` but no header row. See `data.csv` as an example.

example usage:

1. CLI
```shell
curl -X POST http://127.0.0.1:5001/transactions  -F "data=@data.csv"
{"id":1,"key":"5cb78..."}
```

2. Python
```python
>>> import requests
>>> url = 'http://127.0.0.1:5001/'
>>> files = {'data': open('data.csv', 'rb')}
>>> resp = requests.post(url + 'transactions', files=files)
>>> resp.json()
{'id': 0, 'key': '5cb78...'}
```

### `GET /report`
Takes in an `id` and `key` as query arguments and returns a JSON document with the tally of gross revenue, expenses, and net revenue (gross - expenses) as follows:

```
{
    "gross-revenue": <amount>,
    "expenses": <amount>,
    "net-revenue": <amount>
}
```

example usage:

1. CLI
```shell
curl -X GET "http://127.0.0.1:5001/report?id=0&key=5cb78..."
{"expenses":72.93,"gross-revenue":225.0,"net-revenue":152.07}
```

2. Python
```python
>>> import requests
>>> url = 'http://127.0.0.1:5001/'
>>> counter = 0
>>> key = '5cb78...'
>>> resp = requests.get(f'{url}report?id={counter}&key={key}')
>>> resp.json()
{'expenses': 72.93, 'gross-revenue': 225.0, 'net-revenue': 152.07}
```

## approach

My main priority going into this assignment was **simplicity**:
  - Can be implemented and deployed within the given assignment timeframe (2-3 hours).
  - Straightforward implementation that is easily readable by assessment evaluators.

## future work: current shortcomings and solutions
1. **CSV Parsing**: Assumes the user provides a well-formatted CSV file. The curent implementation won't throw an error until the user tries to get a report for a malformed CSV (i.e. `/transactions` does not do format checking when parsing the CSV).
  - Solution(s): Verify CSV formatting and data types manually with error-checking before storing the user's file OR find a robust CSV parsing library so that `/transactions` will return a failure response with a specific parsing error message.

2. **Persistence Scaling**: Currently, the server naively stores all user-uploaded files on disk which could quickly lead to errors once disk space runs out.
  - Solution(s): Use a cloud database with auto-scaling capability. This will likely increase latency but is necessary for serving any reasonably large user base.

3. **Security**: User-uploaded data is stored in plaintext and the hashes (keys) are generated without salts. Bad actors could use collision attacks on the `/report` API to retrieve the aggregate statistics about another user's dataset. However, reversing the hash to get another user's raw input data is still difficult.
  - Solution(s): Look into industry-standard methods of encrypting user data (perhaps some cloud databases already do this). Also, research more secure methods of generating keys.
