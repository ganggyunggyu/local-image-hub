import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

CDP = "http://127.0.0.1:18800"
IMAGE = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs/20260514_instagram_daily_nyangdolsoe_run2_curtain_endcap/nyangdolsoe_curtain_endcap_mineral_gouache_nai_328209216_2_upload.jpg")
SCREENSHOT = Path("/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_20260514_run2_profile_after_upload.png")
CAPTCHA_SCREENSHOT = Path("/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_20260514_run2_captcha_or_challenge.png")
CAPTION = """커튼봉 끝마개가 덜그럭거리면 창가 소리가 계속 신경 쓰임냥
힘으로 꽉 누르기보다 펠트 와셔 하나랑 투명 스페이서로 빈틈을 줄였음냥
조용해진 건 막대기인데 작업실 집중력이 같이 고쳐진 느낌임냥

#냥냥돌쇠 #AI머슴 #생활정비 #커튼정비 #작은물건정비 #작업기록"""

async def check_challenge(page):
    try:
        body = (await page.locator("body").inner_text(timeout=15000)).lower()
    except Exception:
        body = ""
    if "captcha" in body or "challenge" in page.url or "confirm you're not a robot" in body or "로봇" in body:
        CAPTCHA_SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(CAPTCHA_SCREENSHOT), full_page=True)
        print("CAPTCHA_OR_CHALLENGE", page.url)
        print(CAPTCHA_SCREENSHOT)
        return True
    return False

async def click_new_post(page):
    try:
        await page.get_by_role("link", name="새로운 게시물").click(timeout=20000)
        return
    except Exception:
        pass
    await page.evaluate("""
        () => {
          const candidates = [...document.querySelectorAll('a, button')];
          const el = candidates.find(a => (a.innerText || a.getAttribute('aria-label') || '').includes('새로운 게시물'))
            || candidates.find(a => (a.innerText || a.getAttribute('aria-label') || '').includes('만들기'));
          if (el) el.click();
        }
    """)

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

        await click_new_post(page)
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
        await page.wait_for_timeout(7000)
        await page.get_by_role("button", name="공유하기").click(timeout=30000)
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=180000)
        except PlaywrightTimeoutError:
            try:
                await page.wait_for_selector("text=공유 중입니다", state="detached", timeout=180000)
            except Exception:
                pass
        await page.wait_for_timeout(15000)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(10000)
        if await check_challenge(page):
            await browser.close()
            return
        SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(SCREENSHOT), full_page=True)
        links = await page.locator('main a[href*="/p/"]').evaluate_all('(els) => els.slice(0,3).map(a => a.href)')
        body = await page.locator('body').inner_text(timeout=15000)
        print("UPLOAD_DONE", page.url)
        print("RECENT_LINKS", links)
        print("CAPTION_SENT", CAPTION.replace('\n', ' | '))
        print("SCREENSHOT", SCREENSHOT)
        await browser.close()

asyncio.run(main())
