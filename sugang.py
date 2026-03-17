import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# 1. .env 파일에서 정보 불러오기
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
STD_NO = os.getenv("STD_NO")
PWD = os.getenv("PWD")
subjects_str = os.getenv("TARGET_SUBJECTS", "")
target_subjects = subjects_str.split(",")

# 2. 전역 세션(Session) 객체 생성 (자동으로 쿠키 관리)
session = requests.Session()

base_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://sugang.konkuk.ac.kr",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

def send_telegram_message(message):
    """텔레그램으로 메시지를 전송하는 함수"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
        print("텔레그램 알림 전송 완료!")
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def login():
    """서버에 학번과 비밀번호를 보내 로그인하고 쿠키를 발급받는 함수"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 건국대 서버에 자동 로그인을 시도합니다...")
    
    # 방문증(초기 쿠키) 발급을 위한 메인 페이지 사전 방문
    try:
        session.get("https://sugang.konkuk.ac.kr/sugang/login?attribute=loginMain", headers=base_headers)
    except Exception as e:
        print(f"초기 페이지 접속 중 에러가 발생했습니다: {e}")

    fake_time = int(time.time() * 1000)
    login_url = f"https://sugang.konkuk.ac.kr/sugang/login?attribute=loginChk&fake={fake_time}"
    
    # .env 파일에서 가져온 값의 공백 제거
    login_data = {
        "stdNo": STD_NO.strip(),
        "pwd": PWD.strip(),
        "campFg": "1",
        "idPassGubun": "1",
        "lang": "ko"
    }
    
    headers = base_headers.copy()
    headers["Referer"] = "https://sugang.konkuk.ac.kr/sugang/login?attribute=loginMain"
    
    try:
        response = session.post(login_url, data=login_data, headers=headers)
        
        # 세션에 수강신청 전용 쿠키가 잘 들어왔는지 확인
        if "JSUGANGSESSIONID" in session.cookies.get_dict():
            print("자동 로그인 성공! (진짜 재학생 쿠키 발급 완료)\n")
            return True
        else:
            print("로그인 실패: 아이디/비밀번호를 확인해주세요.")
            return False
            
    except Exception as e:
        print(f"로그인 통신 에러: {e}")
        return False

def check_seats(subject_id):
    """여석을 확인하는 함수"""
    fake_time = int(time.time() * 1000)
    url = f"https://sugang.konkuk.ac.kr/sugang/search?attribute=inwonData&pSbjtId={subject_id}&gbn=S&fake={fake_time}"

    headers = base_headers.copy()
    headers["Referer"] = f"https://sugang.konkuk.ac.kr/sugang/core?attribute=coreMain&fake={fake_time}"

    try:
        response = session.post(url, headers=headers)
        
        if not response.text.strip().startswith('{'):
            print("정상적인 데이터를 받지 못했습니다. 세션이 만료되었을 수 있습니다.")
            return False

        data = response.json()
        subject_name = data['rows'][0]['typl_nm']
        inwon_all = data['rows'][0]['inwon_all']
        
        enrolled, capacity = map(int, inwon_all.replace(' ', '').split('/'))
        available_seats = capacity - enrolled
        
        print(f"  - [{subject_name}] 정원: {capacity} / 현재: {enrolled}")
        
        if available_seats > 0:
            msg = f"[{subject_name}] 빈자리 {available_seats}개 발생! \n 이건 내꺼다..!"
            print(msg)
            send_telegram_message(msg)
            
        return True 
            
    except Exception as e:
        print(f"통신 에러: {e}")
        return False


# ---------------------------------------------------------
# 실행 설정 및 메인 루프
# ---------------------------------------------------------
check_interval = 300  # 여석 확인 주기 (5분)

print("건국대학교 수강신청 빈자리 탐지기를 시작합니다! (종료하려면 Ctrl+C)")

# 프로그램 시작 시 1회 로그인 수행
if not login():
    print("프로그램을 종료합니다.")
    exit()

# 세션 갱신 로직을 제거한 초간단 무한 루프
while True:
    now = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{now}] 여석을 확인 중입니다...")
    
    for subject in target_subjects:
        is_ok = check_seats(subject)
        time.sleep(1) # 과목 사이 1초 대기
        
        if not is_ok:
            print("데이터 조회 중 에러 발생. 다음 턴을 기다립니다.")
            
    print(f"{check_interval}초(5분) 대기 후 다시 확인합니다...")
    time.sleep(check_interval)