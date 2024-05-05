import requests
import configparser
import mysql.connector
import time

config = configparser.ConfigParser()
config.read('key.ini')

# 데이터베이스 설정
db_config = {
    'user': config['mysql01']['user'],
    'password': config['mysql01']['password'],
    'host': config['mysql01']['host'],
    'database': config['mysql01']['database'],
    'raise_on_warnings': True
}

API_KEY = config['etherscan']['api_key']


def get_latest_block_transactions(api_key):
    """Etherscan API를 사용하여 최신 블록의 트랜잭션 목록을 조회합니다."""
    # 최신 블록 번호 조회
    block_api_url = "https://api.etherscan.io/api"
    block_params = {
        'module': 'proxy',
        'action': 'eth_blockNumber',
        'apikey': api_key
    }
    block_response = requests.get(block_api_url, params=block_params)
    if block_response.status_code == 200:
        latest_block = int(block_response.json()['result'], 16)
        print(f"Latest Block Number: {latest_block}")
        
        # 최신 블록의 트랜잭션 조회
        tx_params = {
            'module': 'proxy',
            'action': 'eth_getBlockByNumber',
            'tag': hex(latest_block),
            'boolean': 'true',  # 트랜잭션 세부 정보 포함
            'apikey': api_key
        }
        tx_response = requests.get(block_api_url, params=tx_params)
        if tx_response.status_code == 200:
            transactions = tx_response.json()['result']['transactions']
            return transactions
    return 0


def address_balance(address):
    receiver_balance_params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",  # 최신 블록의 잔액 조회
        "apikey": API_KEY
    }
    response = requests.get("https://api.etherscan.io/api", params=receiver_balance_params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1":
            balance = int(data["result"]) / 10**18  # Wei 단위를 ETH로 변환
            return balance
        
    return 0


# 데이터베이스에 연결
db = mysql.connector.connect(**db_config)
cursor = db.cursor()


# cursor.execute("SELECT id, address FROM address order by id asc")
# addresses = cursor.fetchall()
# file_path = 'address.txt'
# with open(file_path, 'w', encoding='utf-8') as file:  # Set encoding to utf-8
#     for id, address in addresses[2544:]:
#         file.write(f"{id}: {address}\n")



cursor.execute("SELECT address FROM address order by id asc")
addresses = cursor.fetchall()

for address in addresses[5267:]:
    address = address[0]

    balance = address_balance(address)

    query = "INSERT INTO address2 (address, balance) VALUES (%s, %s) ON DUPLICATE KEY UPDATE balance=%s"
    cursor.execute(query, (address, balance, balance))
    db.commit()

    time.sleep(0.1)



cursor.close()
db.close()




