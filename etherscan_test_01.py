import requests
import configparser

config = configparser.ConfigParser()
config.read('key.ini')


# Etherscan API 엔드포인트 URL
API_ENDPOINT = "https://api.etherscan.io/api"

# 이더리움 주소
ETHEREUM_ADDRESS = "0x0123456789012345678901234567890123456789"

# Etherscan API 키 (무료 키를 발급받아야 함)
API_KEY = config['etherscan']['API_KEY']

# 파라미터 설정
params = {
    "module": "account",
    "action": "txlist",
    "address": ETHEREUM_ADDRESS,
    "startblock": 0,  # 조회 시작 블록 번호 (0 = genesis 블록부터)
    "endblock": 99999999,  # 조회 종료 블록 번호 (99999999 = 최신 블록까지)
    "sort": "desc",  # 정렬 방식 (desc = 최신 트랜잭션부터)
    "apikey": API_KEY
}

# Etherscan API 요청
response = requests.get(API_ENDPOINT, params=params)

# 응답 데이터 처리
if response.status_code == 200:
    data = response.json()
    if data["status"] == "1":
        transactions = data["result"]
        for tx in transactions:
            print(f"트랜잭션 해시: {tx['hash']}")
            print(f"송신자 주소: {tx['from']}")
            print(f"수신자 주소: {tx['to']}")
            print(f"전송 금액: {tx['value']} WEI")
            print("--------------------")
    else:
        print(f"에러 메시지: {data['message']}")
else:
    print(f"API 요청 실패: {response.status_code}")