import requests
import hashlib
import hmac
import time

api_key = 'your_api_key'
api_secret = 'your_api_secret'
base_url = 'https://api.mexc.com'

def mexc_signature(query_string, secret):
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def send_eth(amount, to_address):
    path = '/api/v2/private/withdraw'
    params = {
        'api_key': api_key,
        'currency': 'ETH',
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
amount = '0.1'  # 송금할 이더리움의 양
to_address = '대상 이더리움 주소'  # 송금할 주소
result = send_eth(amount, to_address)
print(result)
