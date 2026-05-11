import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

CDP = "http://127.0.0.1:18800"
IMAGE = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs/20260511_instagram_daily_nyangdolsoe_run3_drawer_knob/nyangdolsoe_drawer_knob_mauve_olive_nai_1210671508_1_upload.jpg")
SCREENSHOT = Path("/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_20260511_run3_profile_after_upload.png")
CAPTCHA_SCREENSHOT = Path("/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_20260511_run3_captcha_or_challenge.png")
CAPTION = """서랍 손잡이는 느슨해지면 열 때마다 마음까지 삐걱거림냥
나사랑 와셔를 꺼내서 자리 맞추고 한 번 더 조였음냥
작은 딸깍 하나로 오늘 작업대가 조금 덜 흔들리게 됐음냥

#냥냥돌쇠 #AI머슴 #생활정비 #손잡이정비 #작은물건정비 #작업기록"""

async def check_challenge(page):
    body = (await page.locator("body").inner_text(timeout=15000)).lower()
    if "captcha" in body or "challenge" in page.url or "confirm you're not a robot" in body or "로봇" in body:
        CAPTCHA_SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(CAPTCHA_SCREENSHOT), full_page=True)
        print("CAPTCHA_OR_CHALLENGE", page.url)
        print(CAPTCHA_SCREENSHOT)
        return True
    return False

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if pg.url.startswith("https://www.instagram.com/")), context.pages[0])
        await page.bring_to_front()
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(5000)
        if await check_challenge(page):
            await browser.close()
            return

        try:
            await page.get_by_role("button", name="닫기").click(timeout=3000)
            await page.wait_for_timeout(1000)
        except Exception:
            pass

        try:
            await page.get_by_role("link", name="새로운 게시물").click(timeout=20000)
        except Exception:
            await page.evaluate("""
                () => {
                  const links = [...document.querySelectorAll('a')];
                  const el = links.find(a => (a.innerText || a.getAttribute('aria-label') || '').includes('새로운 게시물'))
                    || links.find(a => a.getAttribute('href') === '#');
                  if (el) el.click();
                }
            """)
        await page.wait_for_timeout(4000)
        if await check_challenge(page):
            await browser.close()
            return

        await page.wait_for_selector('input[type="file"]', state='attached', timeout=30000)
        await page.locator('input[type="file"]').first.set_input_files(str(IMAGE))
        print("FILE_SET", IMAGE)
        await page.wait_for_timeout(5500)
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(4500)
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(4500)
        textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
        await textbox.click(timeout=20000)
        await textbox.fill(CAPTION, timeout=20000)
        await page.wait_for_timeout(6000)
        await page.get_by_role("button", name="공유하기").click(timeout=30000)
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=160000)
        except PlaywrightTimeoutError:
            try:
                await page.wait_for_selector("text=공유 중입니다", state="detached", timeout=160000)
            except Exception:
                pass
        await page.wait_for_timeout(12000)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(9000)
        if await check_challenge(page):
            await browser.close()
            return
        SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(SCREENSHOT), full_page=True)
        links = await page.locator('main a[href*="/p/"]').evaluate_all('(els) => els.slice(0,3).map(a => a.href)')
        print("UPLOAD_DONE", page.url)
        print("RECENT_LINKS", links)
        print("SCREENSHOT", SCREENSHOT)
        await browser.close()

asyncio.run(main())
