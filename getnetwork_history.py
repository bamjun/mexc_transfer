import requests
import hashlib
import hmac
import time
import configparser


config = configparser.ConfigParser()
config.read('key.ini')


def generate_signature(secret_key, query_string):
    """Generate HMAC SHA256 signature."""
    return hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def get_currency_config_and_save_to_file(api_url, api_key, api_secret, file_path):
    """Fetches currency configurations from the API and saves them to a text file."""
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    query_string = f"timestamp={timestamp}"
    signature = generate_signature(api_secret, query_string)
    
    headers = {
        'X-MEXC-APIKEY': api_key
    }
    params = {
        'timestamp': timestamp,
        'signature': signature
    }
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code == 200:
        currency_data = response.json()
        with open(file_path, 'w', encoding='utf-8') as file:  # Set encoding to utf-8
            for currency in currency_data:
                for key in currency.keys():
                    file.write(f"{key}: {currency.get(key)}\n")

                file.write("------------------------------------\n")


        print(f"Data successfully written to {file_path}")
    else:
        print("Failed to fetch data:", response.status_code, response.text)

# Example usage
api_url = 'https://api.mexc.com/api/v3/capital/withdraw/history'
api_key = config['history']['API_KEY']
api_secret = config['history']['API_SECRET']
file_path = 'currency_network_history.txt'  # Path to the text file where data will be saved
get_currency_config_and_save_to_file(api_url, api_key, api_secret, file_path)
