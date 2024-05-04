import mysql.connector
import requests
import configparser

# 설정 파일에서 API 키 읽기
config = configparser.ConfigParser()
config.read('key.ini')
API_KEY = config['etherscan']['api_key']

# Etherscan API 엔드포인트 및 이더리움 주소
API_ENDPOINT = "https://api.etherscan.io/api"
RECEIVER_ADDRESS = "0x0123456789012345678901234567890123456789"

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

# Etherscan API 요청 (수신자 잔액 조회)
receiver_balance_params = {
    "module": "account",
    "action": "balance",
    "address": RECEIVER_ADDRESS,
    "tag": "latest",  # 최신 블록의 잔액 조회
    "apikey": API_KEY
}
response = requests.get(API_ENDPOINT, params=receiver_balance_params)

# 수신자 잔액 데이터 처리
if response.status_code == 200:
    data = response.json()
    if data["status"] == "1":
        balance = int(data["result"]) / 10**18  # Wei 단위를 ETH로 변환
        print(f"{RECEIVER_ADDRESS} 주소의 ETH 잔액: {balance} ETH")
        
        # 데이터베이스에 데이터 삽입
        query = "INSERT INTO address (address, balance) VALUES (%s, %s) ON DUPLICATE KEY UPDATE balance=%s"
        cursor.execute(query, (RECEIVER_ADDRESS, balance, balance))
        db.commit()
        
        print(f"데이터베이스에 저장 완료: {RECEIVER_ADDRESS} 잔액 {balance} ETH")
    else:
        print(f"에러 메시지: {data['message']}")
else:
    print(f"API 요청 실패: {response.status_code}")

# 데이터베이스 연결 종료
cursor.close()
db.close()
