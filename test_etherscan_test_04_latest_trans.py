import requests
import configparser

config = configparser.ConfigParser()
config.read('key.ini')



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
    return None

# 사용자 입력 정보

api_key = config['etherscan']['api_key']
# 최신 블록의 트랜잭션 조회 및 출력
transactions = get_latest_block_transactions(api_key)
if transactions:
    for tx in transactions[:5]:  # 최근 5개의 트랜잭션만 출력
        print(f"TxHash: {tx['hash']}")
        print(f"From: {tx['from']}")
        print(f"To: {tx['to']}")
        print(f"Value: {int(tx['value'], 16) / 10**18} Eth")
        print('-' * 60)
else:
    print("Failed to retrieve transactions")
