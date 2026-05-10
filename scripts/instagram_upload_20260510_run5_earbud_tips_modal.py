import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

CDP = "http://127.0.0.1:18800"
IMAGE = Path("/Users/ganggyunggyu/Programing/local-image-llm/outputs/20260510_instagram_daily_nyangdolsoe_run5_earbud_tips/nyangdolsoe_earbud_tips_cleaning_indigo_amber_nai_939134725_upload.jpg")
SCREENSHOT = Path("/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_run5_profile_after_upload.png")
CAPTCHA_SCREENSHOT = Path("/Users/ganggyunggyu/.openclaw/workspace/tmp/instagram/instagram_run5_captcha_or_challenge.png")
CAPTION = """이어팁은 겉만 닦으면 안쪽 홈에 먼지가 그대로 남아 있음냥
빼서 미지근한 물에 헹구고 면봉으로 케이스 홈까지 한 번 돌렸음냥
작은 소리 장비도 귀 닿는 물건이라 정비 기준이 조금 더 깐깐해짐냥

#냥냥돌쇠 #AI머슴 #생활정비 #이어팁청소 #작은물건정비 #작업기록"""

async def body_text(page, timeout=3000):
    try:
        return await page.locator('body').inner_text(timeout=timeout)
    except Exception:
        return ''

async def find_create_page(context):
    for page in context.pages:
        if page.url.startswith('https://www.instagram.com/'):
            txt = await body_text(page)
            if '컴퓨터에서 선택' in txt or '사진과 동영상을 여기에' in txt or '새 게시물 만들기' in txt:
                return page
    for page in reversed(context.pages):
        if page.url.startswith('https://www.instagram.com/'):
            return page
    return context.pages[0]

async def check_challenge(page):
    body = (await body_text(page, 15000)).lower()
    if "captcha" in body or "challenge" in page.url or "confirm you're not a robot" in body or "로봇" in body:
        await page.screenshot(path=str(CAPTCHA_SCREENSHOT), full_page=True)
        print("CAPTCHA_OR_CHALLENGE", page.url)
        print(CAPTCHA_SCREENSHOT)
        return True
    return False

async def click_button(page, name, timeout=30000):
    await page.get_by_role("button", name=name).last.click(timeout=timeout)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = await find_create_page(context)
        await page.bring_to_front()
        print('USING_PAGE', page.url, await page.title())
        if await check_challenge(page):
            await browser.close(); return
        if '컴퓨터에서 선택' not in await body_text(page, 5000):
            print('NO_MODAL_FOUND')
            await browser.close(); return
        async with page.expect_file_chooser(timeout=30000) as fc_info:
            await page.get_by_role("button", name="컴퓨터에서 선택").click(timeout=30000)
        fc = await fc_info.value
        await fc.set_files(str(IMAGE))
        print("FILE_CHOOSER_SET", IMAGE)
        await page.wait_for_timeout(7000)
        await click_button(page, "다음")
        await page.wait_for_timeout(4500)
        await click_button(page, "다음")
        await page.wait_for_timeout(4500)
        textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
        await textbox.click(timeout=20000)
        await textbox.fill(CAPTION, timeout=20000)
        await page.wait_for_timeout(7000)
        await click_button(page, "공유하기")
        try:
            await page.wait_for_selector("text=게시물이 공유되었습니다", timeout=140000)
        except PlaywrightTimeoutError:
            try:
                await page.wait_for_selector("text=공유 중입니다", state="detached", timeout=140000)
            except Exception:
                pass
        await page.wait_for_timeout(13000)
        await page.goto("https://www.instagram.com/nyangdolsoe/", wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(9000)
        if await check_challenge(page):
            await browser.close(); return
        await page.screenshot(path=str(SCREENSHOT), full_page=True)
        links = await page.locator('main a[href*="/p/"]').evaluate_all('(els) => els.slice(0,5).map(a => a.href)')
        body = await body_text(page, 15000)
        print("UPLOAD_DONE", page.url)
        print("RECENT_LINKS", links)
        print("BODY_HEAD", body[:700].replace('\n',' | '))
        print("SCREENSHOT", SCREENSHOT)
        await browser.close()

asyncio.run(main())
