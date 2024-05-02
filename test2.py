# import requests
# import hashlib
# import hmac
# import time
# import configparser


# config = configparser.ConfigParser()
# config.read('key.ini')


# api_key = config['key']['API_KEY']
# api_secret = config['key']['API_SECRET']
# base_url = 'https://api.mexc.com'

# def generate_signature(query_string, secret):
#     return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

# def withdraw_crypto(coin, address, amount, network, memo=None, withdrawOrderId=None, remark=None):
#     # Prepare request
#     timestamp = int(time.time() * 1000)
#     params = {
#         'coin': coin,
#         'address': address,
#         'amount': amount,
#         'network': network,
#         'timestamp': timestamp,
#         'withdrawOrderId': withdrawOrderId,
#         'memo': memo,
#         'remark': remark
#     }
#     # Remove None values
#     params = {k: v for k, v in params.items() if v is not None}
    
#     # Generate the query string and signature
#     query_string = '&'.join([f'{k}={v}' for k, v in sorted(params.items())])
#     signature = generate_signature(query_string, api_secret)
#     params['signature'] = signature
    
#     # Complete the URL with the query string
#     url = f"{base_url}/api/v3/capital/withdraw/apply"
    
#     # Set headers
#     headers = {
#         'X-MEXC-APIKEY': api_key,
#         'Content-Type': 'application/json'
#     }
    
#     # Make the POST request
#     response = requests.post(url, headers=headers, params=params)
#     return response.json()

# # Example usage
# coin = 'PANDORAGPT'
# address = '0x965Df5Ff6116C395187E288e5C87fb96CfB8141c'
# amount = '3'
# network = 'Ethereum(ERC20)'
# memo = 'MX10086'
# response = withdraw_crypto(coin, address, amount, network, memo)
# print(response)



# import requests
# import hashlib
# import hmac
# import time
# from urllib.parse import urlencode
# import configparser


# config = configparser.ConfigParser()
# config.read('key.ini')


# def generate_signature(api_secret, params):
#     """Generate HMAC SHA256 signature."""
#     # Ensure the parameters are sorted by key
#     sorted_params = sorted(params.items())
#     # Create a query string from sorted parameters
#     query_string = urlencode(sorted_params)
#     # Generate the HMAC SHA256 signature
#     signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
#     return signature

# def post_withdraw(api_url, api_key, api_secret, params):
#     """Post a withdrawal request to the API."""
#     headers = {
#         'Content-Type': 'application/json',
#         'X-MEXC-APIKEY': api_key
#     }
    
#     # Add timestamp to the parameters
#     params['timestamp'] = int(time.time() * 1000)
#     # Generate signature
#     params['signature'] = generate_signature(api_secret, params)
    
#     # Encode parameters for the body of the POST request
#     encoded_params = urlencode(params)
    
#     # Make the POST request
#     response = requests.post(api_url, headers=headers, data=encoded_params)
#     return response.json()

# # Example usage
# api_url = 'https://api.mexc.com/api/v3/capital/withdraw/apply'
# api_key = config['key']['API_KEY']
# api_secret = config['key']['API_SECRET']

# params = {
#     'coin': 'PANDORAGPT',
#     'address': '0x965Df5Ff6116C395187E288e5C87fb96CfB8141c',
#     'amount': '3',
#     'network': 'Ethereum(ERC20)',
#     'memo': 'MX10086'
# }

# result = post_withdraw(api_url, api_key, api_secret, params)
# print(result)




import requests
import hashlib
import hmac
import time
import configparser


config = configparser.ConfigParser()
config.read('key.ini')



def generate_signature(secret, params):
    """Generate HMAC SHA256 signature."""
    # Ensure the parameters are sorted by key and formatted as a query string
    query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    # Create a HMAC SHA256 hash
    signature = hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    return signature

def post_withdraw(api_url, api_key, api_secret, params):
    """Send a withdrawal request to the API."""
    headers = {
        'Content-Type': 'application/json',
        'X-MEXC-APIKEY': api_key
    }
    
    # Add the current timestamp to the parameters
    params['timestamp'] = int(time.time() * 1000)
    # Generate and add the signature to the parameters
    params['signature'] = generate_signature(api_secret, params)
    
    # Send the POST request with the parameters encoded in the URL
    response = requests.post(api_url, headers=headers, data=params)
    return response.json()

# Example usage
api_url = 'https://api.mexc.com/api/v3/capital/withdraw/apply'
api_key = config['key']['API_KEY']
api_secret = config['key']['API_SECRET']

params = {
    'coin': 'PANDORAGPT',
    'address': '0x965Df5Ff6116C395187E288e5C87fb96CfB8141c',
    'amount': '3',
    'network': 'Ethereum(ERC20)',
    'memo': 'MX10086'
}

result = post_withdraw(api_url, api_key, api_secret, params)
print(result)

