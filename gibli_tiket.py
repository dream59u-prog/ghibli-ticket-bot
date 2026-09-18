import requests
from playwright.sync_api import sync_playwright


URL = "https://l-tike.com/bw-ticket/ghibli/ghibli-park/"


print("=" * 60)
print("TEST 1 : requests")
print("=" * 60)

try:
    r = requests.get(
        URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            )
        },
        timeout=20
    )

    print("STATUS:", r.status_code)
    print("URL:", r.url)
    print("LENGTH:", len(r.content))

except Exception as e:
    print("REQUESTS ERROR:", repr(e))


print()
print("=" * 60)
print("TEST 2 : Playwright Chromium")
print("=" * 60)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-http2",
        ]
    )

    page = browser.new_page()

    try:

        response = page.goto(
            URL,
            wait_until="commit",
            timeout=60000
        )

        print(
            "STATUS:",
            response.status if response else "NONE"
        )

        print("URL:", page.url)

        page.wait_for_timeout(5000)

        print("TITLE:", page.title())

        page.screenshot(
            path="lticket_test.png",
            full_page=True
        )

        with open(
            "lticket_test.html",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(page.content())

        print("SUCCESS")

    except Exception as e:

        print("PLAYWRIGHT ERROR:")
        print(repr(e))

    finally:

        browser.close()
