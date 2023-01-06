import requests
from dotenv import dotenv_values


def config():
    url = str(dotenv_values(".env").get('SCANNER_API_URL') + '/api')

    headers = {
        'accept': 'application/json',
        'unique': dotenv_values(".env").get('SCANNER_UNIQUE_ID'),
        'token': dotenv_values(".env").get('SCANNER_AUTH_TOKEN'),
        'app-version': '0.02',
        'app-type': 'python',
    }

    return {'url': url, 'headers': headers}


def get_jobs():
    params = {'type': 'python'}

    req = requests.get(config().get('url') + '/external-jobs', params=params, headers=config().get('headers'))

    data = req.json()

    return data


def success_job(data):
    data = {'data': data}

    req = requests.post(config().get('url') + '/external-jobs', json=data, headers=config().get('headers'))

    data = req.json()

    return data
