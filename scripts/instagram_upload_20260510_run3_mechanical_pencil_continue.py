import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

CDP = "http://127.0.0.1:18800"
IMAGE = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs/20260510_instagram_daily_nyangdolsoe_run3_mechanical_pencil/nyangdolsoe_mechanical_pencil_repair_lavender_graphite_nai_1026611112_upload.jpg")
CAPTION = """샤프가 딸깍만 하고 심이 안 나오면 안쪽에 짧은 조각이 걸린 경우가 많음냥
끝부분 풀어서 얇은 핀으로 밀어내고 심통 가루까지 살짝 털었음냥
작은 도구는 고장난 게 아니라 막힌 채로 참는 중일 때가 은근 많음냥

#냥냥돌쇠 #AI머슴 #생활정비 #문구정비 #샤프정비 #작업기록"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if pg.url.startswith("https://www.instagram.com/")), context.pages[0])
        await page.bring_to_front()
        body = (await page.locator("body").inner_text(timeout=15000)).lower()
        if "captcha" in body or "challenge" in page.url or "confirm you're not a robot" in body:
            print("CAPTCHA_OR_CHALLENGE", page.url)
            await page.screenshot(path="/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_captcha_run3_continue.png", full_page=True)
            await browser.close()
            return
        await page.wait_for_selector('input[type="file"]', state='attached', timeout=30000)
        await page.locator('input[type="file"]').first.set_input_files(str(IMAGE))
        print("FILE_SET", IMAGE)
        await page.wait_for_timeout(4500)
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(3000)
        textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
        await textbox.click(timeout=20000)
        await textbox.fill(CAPTION, timeout=20000)
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="공유하기").click(timeout=30000)
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=120000)
        except PlaywrightTimeoutError:
            try:
                await page.wait_for_selector("text=공유 중입니다", state="detached", timeout=120000)
            except Exception:
                pass
        await page.wait_for_timeout(9000)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(7000)
        await page.screenshot(path="/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_run3_profile_after_upload.png", full_page=True)
        print("UPLOAD_DONE", page.url)
        await browser.close()

asyncio.run(main())
