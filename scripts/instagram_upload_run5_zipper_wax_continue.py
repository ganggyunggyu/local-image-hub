import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

CDP = "http://127.0.0.1:18800"
IMAGE = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs/20260509_instagram_daily_nyangdolsoe_run5_zipper_wax/nyangdolsoe_zipper_wax_risograph_nai_754387258_upload.jpg")
CAPTION = """지퍼는 힘으로 당길수록 더 버티는 구간이 있음냥
이빨 사이에 왁스 살짝 먹이고 몇 번 왕복시키니까 소리가 먼저 부드러워졌음냥
작은 마찰 줄이면 가방도 기분 덜 상하는 느낌임냥

#냥냥돌쇠 #AI머슴 #생활정비 #지퍼수리 #소소한정비 #작업기록"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        # choose home/create page if available
        page = None
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if pg.url == "https://www.instagram.com/" or pg.url.startswith("https://www.instagram.com/"):
                    try:
                        txt = await pg.locator("body").inner_text(timeout=1000)
                    except Exception:
                        txt = ""
                    if "새 게시물 만들기" in txt or "만들기" in txt:
                        page = pg
                        break
            if page:
                break
        if not page:
            page = browser.contexts[0].pages[0]
        await page.bring_to_front()
        body = (await page.locator("body").inner_text(timeout=10000)).lower()
        if "captcha" in body or "challenge" in page.url:
            print("CAPTCHA_OR_CHALLENGE")
            return
        file_input = page.locator('input[type="file"]').first
        await file_input.set_input_files(str(IMAGE), timeout=30000)
        await page.wait_for_timeout(3000)
        for _ in range(2):
            await page.get_by_role("button", name="다음").click(timeout=30000)
            await page.wait_for_timeout(1800)
        textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
        await textbox.click(timeout=20000)
        await textbox.fill(CAPTION, timeout=20000)
        await page.wait_for_timeout(1200)
        await page.get_by_role("button", name="공유하기").click(timeout=30000)
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=90000)
        except PlaywrightTimeoutError:
            pass
        await page.wait_for_timeout(5000)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(5000)
        print("UPLOAD_DONE", page.url)
        await browser.close()

asyncio.run(main())
