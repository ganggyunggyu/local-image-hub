import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

CDP = "http://127.0.0.1:18800"
IMAGE = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs/20260510_instagram_daily_nyangdolsoe_run1_shoelace_aglet/nyangdolsoe_shoelace_aglet_cyanotype_nai_872473229_upload.jpg")
CAPTION = """신발끈 끝이 풀리면 묶을 때마다 손끝에 자꾸 걸림냥
투명 수축튜브 짧게 끼우고 열만 살짝 먹였더니 다시 길이 잡혔음냥
큰 수선 아니어도 매일 잡는 작은 끝부터 정리하면 문앞이 덜 부산함냥

#냥냥돌쇠 #AI머슴 #생활정비 #신발끈정비 #현관정리 #작업기록"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = next((pg for pg in context.pages if "instagram.com" in pg.url), None)
        if page is None:
            page = await context.new_page()
        await page.bring_to_front()
        await page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(3000)
        body = (await page.locator("body").inner_text(timeout=10000)).lower()
        if "captcha" in body or "challenge" in page.url or "suspicious" in body:
            print("CAPTCHA_OR_CHALLENGE", page.url)
            return
        # clear leftover modals
        for _ in range(3):
            try:
                close = page.get_by_role("button", name="닫기")
                if await close.count():
                    await close.first.click(timeout=2000)
                    await page.wait_for_timeout(700)
                    try:
                        await page.get_by_role("button", name="삭제").click(timeout=1500)
                    except Exception:
                        pass
            except Exception:
                pass
        try:
            await page.get_by_role("link", name="새로운 게시물").click(timeout=15000)
        except Exception:
            await page.locator('svg[aria-label="새로운 게시물"]').locator('xpath=ancestor::a[1]').click(timeout=8000)
        try:
            await page.wait_for_selector('input[type="file"]', state='attached', timeout=8000)
        except PlaywrightTimeoutError:
            try:
                await page.get_by_role("link", name="게시물").click(timeout=8000)
            except Exception:
                await page.get_by_text("게시물", exact=True).click(timeout=8000)
            await page.wait_for_selector('input[type="file"]', state='attached', timeout=30000)
        await page.locator('input[type="file"]').first.set_input_files(str(IMAGE))
        print("FILE_SET", IMAGE)
        await page.wait_for_timeout(3500)
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(2200)
        await page.get_by_role("button", name="다음").click(timeout=30000)
        await page.wait_for_timeout(2200)
        textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
        await textbox.click(timeout=20000)
        await textbox.fill(CAPTION, timeout=20000)
        await page.wait_for_timeout(1600)
        await page.get_by_role("button", name="공유하기").click(timeout=30000)
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=90000)
        except PlaywrightTimeoutError:
            try:
                await page.wait_for_selector("text=공유 중입니다", state="detached", timeout=90000)
            except Exception:
                pass
        await page.wait_for_timeout(4500)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(5000)
        print("UPLOAD_DONE", page.url)
        await browser.close()

asyncio.run(main())
