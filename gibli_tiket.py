import os
import requests
from playwright.sync_api import sync_playwright

# 환경 변수에서 카카오 엑세스 토큰 로드 (보안)
KAKAO_ACCESS_TOKEN = os.environ.get("KAKAO_ACCESS_TOKEN")

def send_kakao_message(message_text):
    """카카오톡 '나에게 보내기' API 호출"""
    if not KAKAO_ACCESS_TOKEN:
        print("[ERROR] KAKAO_ACCESS_TOKEN 이 설정되지 않았습니다.")
        return

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {KAKAO_ACCESS_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload = {
        "template_object": f'''{{
            "object_type": "text",
            "text": "{message_text}",
            "link": {{
                "web_url": "https://l-tike.com/bw-ticket/ghibli/ghibli-park/",
                "mobile_web_url": "https://l-tike.com/bw-ticket/ghibli/ghibli-park/"
            }},
            "button_title": "부우 티켓 예매 바로가기"
        }}'''
    }

    res = requests.post(url, headers=headers, data=payload)
    if res.status_code == 200:
        print("[성공] 카카오톡 알림을 발송했습니다.")
    else:
        print(f"[실패] 카카오톡 발송 오류: {res.status_code} - {res.text}")

def check_boo_woo_ticket():
    # 부우 티켓 지브리 파크 예매 페이지 URL
    TARGET_URL = "https://l-tike.com/bw-ticket/ghibli/ghibli-park/"
    TARGET_DATE = "20261003"  # 2026년 10월 3일
    
    with sync_playwright() as p:
        # 봇 탐지 우회를 위한 User-Agent 설정
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("[진행 중] Boo-Woo 예매 사이트 접속 중...")
            page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)

            # 렌더링 대기
            page.wait_for_timeout(3000)
            
            content = page.content()

            # 부우 티켓 페이지 내에서 10/3 매진(× 또는 完売) 표시가 풀렸는지 검사
            # (※ 부우 티켓 UI 갱신 시 셀렉터 및 텍스트 조건 점검 권장)
            is_sold_out = "完売" in content or "×" in content
            is_date_exist = "10월 3일" in content or "10/3" in content or TARGET_DATE in content

            # 잔여 자리가 감지된 조건 (매진 키워드가 없는 경우)
            if is_date_exist and not is_sold_out:
                msg = "[🚨 지브리 파크 취소표 감지!]\n2026년 10월 3일(토) 2인 티켓 잔여 자리가 발생했습니다!\n지금 바로 Boo-Woo에 접속하세요."
                print(msg)
                send_kakao_message(msg)
            else:
                print(f"[알림] 2026-10-03 잔여 티켓이 없습니다. (다음 스케줄 대기)")

        except Exception as e:
            print(f"[오류 발생] 크롤링 도중 예외 발생: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check_boo_woo_ticket()