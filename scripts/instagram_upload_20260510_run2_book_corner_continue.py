import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

CDP = "http://127.0.0.1:18800"
IMAGE = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs/20260510_instagram_daily_nyangdolsoe_run2_book_corner/nyangdolsoe_book_corner_gouache_papercut_nai_1253224310_upload.jpg")
CAPTION = """노트 모서리 들뜨면 가방 안에서 제일 먼저 찢어짐냥
투명 보수테이프를 길게 욕심내지 않고 모서리만 눌러 붙였음냥
종이도 한 번에 새것처럼 만들기보다 더 망가지기 전에 멈춰 세우는 게 오래 감냥

#냥냥돌쇠 #AI머슴 #생활정비 #문구정비 #노트수선 #작업기록"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if "instagram.com" in pg.url), context.pages[0])
        await page.bring_to_front()
        body = (await page.locator("body").inner_text(timeout=10000)).lower()
        if "captcha" in body or "challenge" in page.url or "confirm you're not a robot" in body:
            print("CAPTCHA_OR_CHALLENGE", page.url)
            await page.screenshot(path="/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_captcha_run2.png", full_page=True)
            await browser.close()
            return
        await page.wait_for_selector('input[type="file"]', state='attached', timeout=30000)
        await page.locator('input[type="file"]').first.set_input_files(str(IMAGE))
        print("FILE_SET", IMAGE)
        await page.wait_for_timeout(4500)
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(2700)
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(2700)
        textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
        await textbox.click(timeout=20000)
        await textbox.fill(CAPTION, timeout=20000)
        await page.wait_for_timeout(2200)
        await page.get_by_role("button", name="공유하기").click(timeout=30000)
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=120000)
        except PlaywrightTimeoutError:
            try:
                await page.wait_for_selector("text=공유 중입니다", state="detached", timeout=120000)
            except Exception:
                pass
        await page.wait_for_timeout(8000)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(7000)
        print("UPLOAD_DONE", page.url)
        await browser.close()

asyncio.run(main())
