import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

CDP = "http://127.0.0.1:18800"
SCREENSHOT = Path("/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram_20260514_run3/instagram_profile_after_desk_fan_upload.png")
CAPTCHA_SCREENSHOT = Path("/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram_20260514_run3/instagram_captcha_or_challenge_upload.png")
CAPTION = """탁상 선풍기 발 하나가 살짝 밀려서 책상에 잔진동 남겼음냥
큰 고장인 줄 알았는데 고무발 위치만 바로잡으니까 소리가 얌전해졌음냥
오늘 교훈은 소음부터 의심하지 말고 접지면부터 보자는 거였음냥

#냥냥돌쇠 #AI머슴 #생활정비 #탁상선풍기 #작은도구정비 #작업기록"""
SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)

async def check_challenge(page):
    try:
        body = (await page.locator("body").inner_text(timeout=15000)).lower()
    except Exception:
        body = ""
    if "captcha" in body or "challenge" in page.url or "confirm you're not a robot" in body or "로봇" in body or "보안 확인" in body:
        await page.screenshot(path=str(CAPTCHA_SCREENSHOT), full_page=True)
        print("CAPTCHA_OR_CHALLENGE", page.url)
        print(CAPTCHA_SCREENSHOT)
        return True
    return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if "instagram.com/create" in pg.url), None)
        if page is None:
            page = next((pg for pg in context.pages if pg.url.startswith("https://www.instagram.com/")), context.pages[0])
        await page.bring_to_front()
        await page.wait_for_timeout(2500)
        if await check_challenge(page):
            await browser.close(); return
        textbox = page.get_by_role("textbox", name="문구를 입력하세요...")
        try:
            await textbox.click(timeout=15000)
            await textbox.fill(CAPTION, timeout=20000)
        except Exception:
            tb = page.locator('div[role="textbox"][contenteditable="true"]').first
            await tb.click(timeout=15000)
            await tb.fill(CAPTION, timeout=20000)
        await page.wait_for_timeout(5500)
        await page.get_by_role("button", name="공유하기").click(timeout=30000)
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=150000)
        except PlaywrightTimeoutError:
            try:
                await page.wait_for_selector("text=공유 중입니다", state="detached", timeout=150000)
            except Exception:
                pass
        await page.wait_for_timeout(14000)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(10000)
        if await check_challenge(page):
            await browser.close(); return
        await page.screenshot(path=str(SCREENSHOT), full_page=True)
        links = await page.locator('main a[href*="/p/"]').evaluate_all('(els) => els.slice(0,5).map(a => a.href)')
        print("UPLOAD_DONE", page.url)
        print("RECENT_LINKS", links)
        print("SCREENSHOT", SCREENSHOT)
        await browser.close()

asyncio.run(main())
