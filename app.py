import requests
from bs4 import BeautifulSoup

def get_exchange_rate(code):
    # 네이버 금융 환율 상세 페이지 주소
    url = f"https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_{code}KRW"
    
    # 로봇 차단을 피하기 위한 헤더 설정
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        # 웹페이지 소스에서 환율 숫자가 있는 '.value' 태그 찾기
        rate_text = soup.select_one(".value").get_text()
        return float(rate_text.replace(",", ""))
    except Exception:
        return None

def main():
    print("=== 💰 실시간 네이버 환율 계산기 ===")
    target = input("통화를 입력하세요 (예: USD, JPY, EUR): ").upper()
    amount = float(input(f"환전할 {target} 금액을 입력하세요: "))
    
    rate = get_exchange_rate(target)
    
    if rate:
        # 엔화(JPY)는 보통 100단위 기준이므로 별도 처리
        result = (amount / 100 * rate) if target == "JPY" else (amount * rate)
        print(f"\n[실시간 환율] 1 {target} = {rate} KRW")
        print(f"✅ 결과: {amount:,} {target} -> {result:,.2f} 원")
    else:
        print("❌ 환율 정보를 가져오지 못했습니다. 통화 코드를 확인하세요.")

if __name__ == "__main__":
    main()