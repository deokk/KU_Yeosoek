import requests
import time
from datetime import datetime

# 봇파더에게 받은 텔레그램 토큰과 내 채팅방 ID
TELEGRAM_TOKEN = "8780041592:AAHVFpORihVMrJTtOJSA05vGSSqYlq7HuCA"
CHAT_ID = "8737822477"

def send_telegram_message(message):
    """텔레그램으로 메시지를 전송하는 함수"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
        print("✅ 텔레그램 알림 전송 완료!")
    except Exception as e:
        print(f"❌ 텔레그램 전송 실패: {e}")

def extend_session(headers):
    """세션(로그인 상태)을 연장하는 함수"""
    fake_time = int(time.time() * 1000)
    # 방금 찾아내신 GET 방식의 연장 API 주소 적용
    url = f"https://sugang.konkuk.ac.kr/sugang/core?attribute=coreData&fake={fake_time}"
    
    try:
        # GET 방식이므로 requests.get() 사용
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("🔄 [시스템] 로그인 세션을 성공적으로 연장했습니다! (수명 +10분)")
        return True
    except Exception as e:
        print(f"❌ 세션 연장 실패: {e}")
        return False

def check_seats(subject_id, headers):
    """특정 과목의 여석을 확인하는 함수"""
    fake_time = int(time.time() * 1000)
    url = f"https://sugang.konkuk.ac.kr/sugang/search?attribute=inwonData&pSbjtId={subject_id}&gbn=S&fake={fake_time}"

    try:
        response = requests.post(url, headers=headers)
        
        if not response.text.strip().startswith('{'):
            print("❌ 서버가 정상적인 데이터를 주지 않았습니다. 진짜 이유는 다음과 같습니다:")
            # 서버가 보낸 에러 내용 500자만 잘라서 출력해보기
            print(response.text[:500]) 
            return False

        data = response.json()
        subject_name = data['rows'][0]['typl_nm']
        inwon_all = data['rows'][0]['inwon_all']
        
        enrolled, capacity = map(int, inwon_all.replace(' ', '').split('/'))
        available_seats = capacity - enrolled
        
        print(f"  - [{subject_name}] 정원: {capacity} / 현재: {enrolled}")
        
        if available_seats > 0:
            msg = f"🚨 [{subject_name}] 빈자리 {available_seats}개 발생! 당장 달려가세요! 🚨"
            print(msg)
            send_telegram_message(msg)
            
        return True 
            
    except Exception as e:
        print(f"통신 에러: {e}")
        return False

# ---------------------------------------------------------
# 실행 설정 부분
# ---------------------------------------------------------
MY_COOKIE = 'COOK_TS=1773715452020; _ga=GA1.1.1981277237.1760362428; WMONID=Q2fkfh8FbPO; _ga_B0F4RVY3ZV=GS2.1.s1773624045$o14$g1$t1773624159$j20$l0$h0; JSUGANGSESSIONID=00018KUGk0C3nY2HxFzMPmnbv3i:2R8PTNUABT; my-application-browser-tab={"guid":"a5d6f3e5-f9c2-0883-aa83-c07121132513","timestamp":1773715469590}'

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://sugang.konkuk.ac.kr",
    "Referer": "https://sugang.konkuk.ac.kr/sugang/core?attribute=coreMain&fake=1773582607622",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": MY_COOKIE
}

###############여기에 원하는 과목 코드를 입력#################
target_subjects = ["3233", "3460"]
check_interval = 300  # 여석 확인 주기 (초)

print("🚀 24시간 수강신청 빈자리 탐지기를 시작합니다! (종료하려면 Ctrl+C)")

# 세션 연장 타이머를 위한 변수 초기화
last_extend_time = time.time()

while True:
    now = datetime.now().strftime("%H:%M:%S")
    current_time = time.time()
    
    # 10분동안 아무것도 안할시 로그아웃을 방지하기 위해 세션 연장
    if current_time - last_extend_time >= 500:
        extend_session(headers)
        last_extend_time = current_time # 타이머 초기화

    print(f"\n[{now}] 여석을 확인 중입니다...")
    
    for subject in target_subjects:
        is_ok = check_seats(subject, headers)
        time.sleep(1) 
        
        if not is_ok:
            exit()
            
    time.sleep(check_interval)