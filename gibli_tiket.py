import os
import time
from playwright.sync_api import sync_playwright

KAKAO_ACCESS_TOKEN = os.environ.get("KAKAO_ACCESS_TOKEN")

TARGET_URL = "https://l-tike.com/bw-ticket/ghibli/ghibli-park/"


def test_lticket():

    print("[진행 중] Playwright로 Boo-Woo 접속 테스트")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        context = browser.new_context(
            locale="ja-JP",
            timezone_id="Asia/Tokyo",
            viewport={
                "width": 1366,
                "height": 900
            },
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()

        try:

            print("[1] 페이지 접속 중...")

            response = page.goto(
                TARGET_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("[2] HTTP 상태:", response.status if response else "없음")

            time.sleep(5)

            print("[3] 현재 URL:")
            print(page.url)

            print("[4] 페이지 제목:")
            print(page.title())

            # 화면 저장
            page.screenshot(
                path="lticket_debug.png",
                full_page=True
            )

            # HTML 일부 저장
            html = page.content()

            with open(
                "lticket_debug.html",
                "w",
                encoding="utf-8"
            ) as f:
                f.write(html)

            print("[5] 페이지 저장 완료")

            print("[6] HTML 길이:", len(html))

        except Exception as e:

            print("[오류]", repr(e))

            try:
                page.screenshot(
                    path="lticket_error.png",
                    full_page=True
                )
            except:
                pass

        finally:

            browser.close()


if __name__ == "__main__":
    test_lticket()
