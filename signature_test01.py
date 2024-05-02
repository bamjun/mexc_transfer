import requests
import time
import hmac
import hashlib

import configparser
config = configparser.ConfigParser()
config.read('key.ini')

# MEXC API 키 및 시크릿 키 설정
api_key = config['key']['API_KEY']
secret_key = config['key']['API_SECRET']

# 출금 정보 설정
coin = 'PANDORAGPT'
address = '0x965Df5Ff6116C395187E288e5C87fb96CfB8141c'
amount = '3'
network = 'Ethereum(ERC20)'
memo = 'MX10086'

# 타임스탬프 생성
timestamp = str(int(time.time() * 1000))

# 서명 생성
params = f'coin={coin}&address={address}&amount={amount}&network={network}&memo={memo}&timestamp={timestamp}'
signature = hmac.new(secret_key.encode(), params.encode(), hashlib.sha256).hexdigest()

# API 요청 보내기
url = 'https://api.mexc.com/api/v3/capital/withdraw/apply'
headers = {
    'X-MEXC-APIKEY': api_key,
    'Content-Type': 'application/json'
}
data = {
    'coin': coin,
    'address': address,
    'amount': amount,
    'network': network,
    'memo': memo,
    'timestamp': timestamp,
    'signature': signature
}

response = requests.post(url, headers=headers, data=data)
print(response.json())
