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

def generate_signature(query_string, secret):
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def withdraw_crypto(coin, address, amount, network, memo=None, withdrawOrderId=None, remark=None):
    # Prepare request
    timestamp = int(time.time() * 1000)
    params = {
        'coin': coin,
        'address': address,
        'amount': amount,
        'network': network,
        'timestamp': timestamp,
        'withdrawOrderId': withdrawOrderId,
        'memo': memo,
        'remark': remark
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Generate the query string and signature
    query_string = '&'.join([f'{k}={v}' for k, v in sorted(params.items())])
    signature = generate_signature(query_string, api_secret)
    params['signature'] = signature
    
    # Complete the URL with the query string
    url = f"{base_url}/api/v3/capital/withdraw/apply"
    
    # Set headers
    headers = {
        'X-MEXC-APIKEY': api_key,
        'Content-Type': 'application/json'
    }
    
    # Make the POST request
    response = requests.post(url, headers=headers, params=params)
    return response.json()

# Example usage
coin = 'PANDORAGPT'
address = '0x965Df5Ff6116C395187E288e5C87fb96CfB8141c'
amount = '3'
network = 'ETH'
memo = 'MX10086'
response = withdraw_crypto(coin, address, amount, network, memo)
print(response)
