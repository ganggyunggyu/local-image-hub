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
        context = browser.contexts[0]
        page = None
        for pg in context.pages:
            if "instagram.com" in pg.url:
                page = pg
                break
        if page is None:
            page = await context.new_page()
        await page.bring_to_front()
        await page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(2500)
        body = (await page.locator("body").inner_text(timeout=10000)).lower()
        if "captcha" in body or "challenge" in page.url:
            print("CAPTCHA_OR_CHALLENGE")
            return
        # Clear any leftover modals gently.
        for _ in range(2):
            try:
                close = page.get_by_role("button", name="닫기")
                if await close.count():
                    await close.first.click(timeout=2000)
                    await page.wait_for_timeout(600)
                    try:
                        await page.get_by_role("button", name="삭제").click(timeout=1500)
                    except Exception:
                        pass
            except Exception:
                pass
        # Open create modal.
        try:
            await page.get_by_role("link", name="새로운 게시물").click(timeout=12000)
        except Exception:
            await page.locator('a[href="#"]').filter(has_text="").nth(3).click(timeout=5000)
        await page.wait_for_selector('input[type="file"]', timeout=30000)
        await page.locator('input[type="file"]').first.set_input_files(str(IMAGE))
        await page.wait_for_timeout(3000)
        # Crop step next
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(1800)
        # Edit step next
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(1800)
        # Caption textbox
        textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
        await textbox.click(timeout=20000)
        await textbox.fill(CAPTION, timeout=20000)
        await page.wait_for_timeout(1200)
        await page.get_by_role("button", name="공유하기").click(timeout=30000)
        # Wait for share completion or profile availability.
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=90000)
        except PlaywrightTimeoutError:
            try:
                await page.wait_for_selector("text=공유 중입니다", state="detached", timeout=90000)
            except Exception:
                pass
        await page.wait_for_timeout(3000)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(4000)
        print("UPLOAD_DONE", page.url)
        await browser.close()

asyncio.run(main())
