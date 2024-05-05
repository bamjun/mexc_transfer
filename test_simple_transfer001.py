import requests
import hmac
import hashlib
import json
import mysql.connector
import time

import configparser
config = configparser.ConfigParser()
config.read('key.ini')

# MEXC API 키 및 시크릿 키 설정
api_key = config['key']['API_KEY']
secret_key = config['key']['API_SECRET']



def mexc_withdraw(coin, address, amount):
    # 타임스탬프 생성
    servertime = requests.get('https://api.mexc.com/api/v3/time')
    servertime = servertime.json()
    timestamp = str(servertime['serverTime'])

    # 서명 생성
    params = f'coin={coin}&address={address}&amount={amount}&timestamp={timestamp}'
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
        'timestamp': timestamp,
        'signature': signature
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

# 데이터베이스 설정
db_config = {
    'user': config['mysql01']['user'],
    'password': config['mysql01']['password'],
    'host': config['mysql01']['host'],
    'database': config['mysql01']['database'],
    'raise_on_warnings': True
}






# 데이터베이스에 연결
db = mysql.connector.connect(**db_config)
cursor = db.cursor()


cursor.execute("SELECT address FROM etherscan.address2 where balance > 0 and balance < 2 order by id asc;")
addresses = cursor.fetchall()


coin = 'PANDORAGPT'
amount = '3'

for address in addresses[352:353]:
    address = address[0]
    # print(address)

    with open('withdraw_history.txt', 'a', encoding='utf-8') as file:  # Set encoding to utf-8
        file.write(address)
        file.write(json.dumps(mexc_withdraw(coin, address, amount)) + '\n')


cursor.close()
db.close()

