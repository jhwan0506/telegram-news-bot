# 텔레그램 데일리 뉴스 브리핑 봇

매일 아침 (기본 KST 07:00) 크립토 / 빅테크 / 거시경제 헤드라인을 자동으로 텔레그램 메시지로 보내주는 봇입니다.
서버 없이 GitHub Actions로 완전 자동 실행되고, 완전 무료입니다.

## 설정 방법 (한 번만 하면 끝)

### 1. 텔레그램 봇 만들기
1. 텔레그램에서 `@BotFather` 검색
2. `/newbot` 입력 → 이름/username 설정 → 토큰 발급받기 (예: `123456:ABC-DEF...`)
3. 발급받은 토큰을 잘 저장해두기 → 이게 `TELEGRAM_BOT_TOKEN`

### 2. 내 chat_id 알아내기
1. 방금 만든 봇에게 아무 메시지나 하나 보내기 (예: "안녕")
2. 브라우저로 아래 주소 접속 (토큰 부분만 본인 것으로 교체)
   ```
   https://api.telegram.org/bot<본인의 토큰>/getUpdates
   ```
3. 결과 JSON 안에서 `"chat":{"id": 123456789, ...}` 부분의 숫자가 `TELEGRAM_CHAT_ID`

### 3. GitHub 저장소에 코드 올리기
1. GitHub에 새 저장소(Private으로) 하나 만들기
2. 이 폴더 안의 파일들(`briefing.py`, `requirements.txt`, `.github/workflows/daily-briefing.yml`)을 그대로 업로드

### 4. Secrets 등록하기
1. 저장소 → Settings → Secrets and variables → Actions
2. `New repository secret` 클릭해서 아래 2개 등록
   - `TELEGRAM_BOT_TOKEN` → 1번에서 받은 토큰
   - `TELEGRAM_CHAT_ID` → 2번에서 알아낸 숫자

### 5. 테스트 실행
1. 저장소 → Actions 탭 → "Daily News Briefing" 워크플로 선택
2. `Run workflow` 버튼으로 수동 실행 → 텔레그램으로 메시지 오는지 확인

여기까지 되면 끝입니다. 이후로는 매일 정해진 시각에 자동으로 실행돼서 별도 요청 없이 브리핑이 옵니다.

## 커스터마이징
- `briefing.py`의 `FEEDS` 딕셔너리에 원하는 RSS 주소를 추가/삭제하면 소스 조정 가능
- `MAX_PER_CATEGORY` 값으로 카테고리당 헤드라인 개수 조절
- `daily-briefing.yml`의 cron 시각을 바꾸면 발송 시간 조정 가능 (UTC 기준, KST는 UTC+9)

## 다음 업그레이드 아이디어
- 단순 헤드라인 나열 대신 Claude API로 "3줄 요약"을 붙이면 훨씬 읽기 편해짐
- 보유 코인 시세/펀딩비를 같이 붙여서 개인 맞춤 브리핑으로 확장 가능
