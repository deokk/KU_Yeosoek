# 🚀 KU-Yeosoek (건국대학교 수강신청 빈자리 알림 봇)

> **"수강신청 여석 확인, 이제 직접 새로고침하지 마세요."**
> 건국대학교 수강신청 시스템을 실시간 모니터링하여, 빈자리 발생 시 텔레그램(Telegram)으로 실시간 알림을 보내주는 파이썬 자동화 스크립트입니다.

---

## 핵심 기능 (Key Features)

- **재학생(SID) 자동 로그인**: 세션(Session) 유지 기술을 통해 별도의 로그인 조작 없이 24시간 감시가 가능합니다.
- **실시간 여석 조회**: 5분(설정 가능) 주기로 서버를 체크하여 과목별 정원 및 현재 인원 데이터를 수집합니다.
- **즉각적인 텔레그램 알림**: 빈자리가 1개라도 발생하면 사용자의 스마트폰으로 푸시 알림을 즉시 전송합니다.
- **보안 최적화**: `.env` 파일을 통해 학번, 비밀번호 등 민감 정보를 코드와 분리하여 관리합니다.

##  기술 스택 (Tech Stack)

- **Language**: Python 3.x
- **Libraries**: `requests`, `python-dotenv`, `Telegram Bot API`

##  설치 및 실행 (Quick Start)

아래 명령어를 순서대로 따라하면 즉시 실행 가능합니다.


# 1. 레포지토리 복제 및 이동
```
git clone [https://github.com/deokk/KU_Yeosoek.git](https://github.com/deokk/KU_Yeosoek.git)
cd KU_Yeosoek 
```

# 2. 필수 라이브러리 설치
```
pip install -r requirements.txt
```
## 텔레그램 봇 생성 및 설정 방법

알림을 받기 위해 텔레그램 봇을 생성하고 정보를 획득하는 과정입니다.

### 1. 봇 생성 및 토큰(Token) 획득
1. 텔레그램에서 [@BotFather](https://t.me/botfather)를 검색하여 대화를 시작합니다.
2. `/newbot` 명령어를 입력합니다.
3. 봇의 이름(Name)과 사용자 이름(Username, 'bot'으로 끝나야 함)을 설정합니다.
4. 생성이 완료되면 `HTTP API token` (예: `123456:ABC-DEF...`)을 복사하여 `.env`의 `TELEGRAM_TOKEN`에 입력합니다.

### 2. 채팅방 ID(Chat ID) 확인
1. 텔레그램에서 방금 만든 봇을 검색하여 **[시작(Start)]** 버튼을 누릅니다.
2. 브라우저에서 아래 주소로 접속합니다 (본인의 토큰 입력).
   - `https://api.telegram.org/bot<본인의_토큰>/getUpdates`
3. 브라우저에 뜨는 JSON 내용 중 `"chat":{"id":123456789...}` 부분의 숫자를 복사하여 `.env`의 `CHAT_ID`에 입력합니다.
   - *팁: 봇에게 아무 메시지나 보낸 후 새로고침해야 데이터가 뜹니다!*

### 3. 환경 변수(.env) 설정 (직접 파일을 만들어 아래 내용을 입력하세요)
LEGRAM_TOKEN=텔레그램 봇 토큰
AT_ID=텔레그램 채팅 아이디
STD_NO=학교아이디
PWD=학교비밀번호

### 4. 과목 코드 설정
`target_subjects`에 원하는 과목 코드를 입력

### 5. 실행
```
python sugang.py
```