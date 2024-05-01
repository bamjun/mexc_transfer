import requests
import hashlib
import hmac
import time
import configparser


config = configparser.ConfigParser()
config.read('key.ini')


api_key = config['key']['API_KEY']
api_secret = config['key']['API_SECRET']
base_url = 'https://api.mexc.com'

def mexc_signature(query_string, secret):
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def send_eth(amount, to_address):
    path = '/api/v2/private/withdraw'
    params = {
        'api_key': api_key,
        'currency': 'PANDORAGPT',
        'amount': amount,
        'address': to_address,
        'req_time': int(time.time() * 1000)  # Timestamp in milliseconds
    }
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    signature = mexc_signature(query_string, api_secret)
    headers = {
        'Content-Type': 'application/json',
        'Api-Signature': signature,
        'Api-Key': api_key,
        'Api-Req-Time': str(params['req_time'])
    }
    response = requests.post(base_url + path, headers=headers, json=params)
    return response.json()

# 사용 예시
amount = '3'  # 송금할 이더리움의 양
to_address = '0x965Df5Ff6116C395187E288e5C87fb96CfB8141c'  # 송금할 주소
result = send_eth(amount, to_address)
print(result)
