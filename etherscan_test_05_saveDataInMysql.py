import requests
import mysql.connector
import time
import configparser

config = configparser.ConfigParser()
config.read('key.ini')
API_KEY = config['etherscan']['api_key']
API_ENDPOINT = "https://api.etherscan.io/api"

# MySQL 데이터베이스 연결 설정
db_config = {
    'user': config['mysql01']['user'],
    'password': config['mysql01']['password'],
    'host': config['mysql01']['host'],
    'database': config['mysql01']['database'],
    'raise_on_warnings': True
}
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# 최근 트랜잭션 조회
params_txlist = {
    'module': 'account',
    'action': 'txlist',
    'address': 'known_address',  # 대량 트랜잭션이 발생하는 주소 예시
    'startblock': 0,
    'endblock': 99999999,
    'sort': 'desc',
    'apikey': API_KEY
}
response = requests.get(API_ENDPOINT, params=params_txlist)
addresses = set()

# 응답 데이터 구조 검사
if response.status_code == 200:
    data = response.json()
    if data['status'] == '1' and 'result' in data:
        transactions = data['result']
        print("Transaction data structure:", transactions[0])  # 첫 번째 트랜잭션 데이터 구조 출력

        for tx in transactions:
            if len(addresses) < 5:
                addresses.add(tx['from'])
            else:
                break
    else:
        print(f"Error fetching transactions: {data['message']}")
else:
    print("Failed to fetch transactions:", response.status_code)

time.sleep(2)  # API 요청 간 지연
# 각 주소의 잔액 조회 및 데이터베이스 저장
for address in addresses:
    params_balance = {
        'module': 'account',
        'action': 'balance',
        'address': address,
        'tag': 'latest',
        'apikey': API_KEY
    }
    balance_response = requests.get(API_ENDPOINT, params=params_balance)
    if balance_response.status_code == 200:
        balance_data = balance_response.json()
        balance = int(balance_data['result']) / 10**18
        query = "INSERT INTO address (address, balance) VALUES (%s, %s) ON DUPLICATE KEY UPDATE balance=%s"
        cursor.execute(query, (address, balance, balance))
        db.commit()

cursor.close()
db.close()