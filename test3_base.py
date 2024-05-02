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

