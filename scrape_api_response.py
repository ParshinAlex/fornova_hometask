from playwright.async_api import async_playwright
import json

INITIAL_URL = "https://www.traveloka.com/en-en"
TARGET_URL = "https://www.traveloka.com/en-th/hotel/detail?spec=20-02-2025.21-02-2025.1.1.HOTEL.9000001153383.novotel%20hua%20hin%20cha-am%20beach%20resort%20&%20spa.2"

async def create_stealth_browser():
    p = await async_playwright().start()

    browser = await p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process",
            "--disable-dev-shm-usage",
        ]
    )

    context = await browser.new_context(
        viewport={"width": 2560, "height": 1440},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="America/New_York",
    )

    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
                                  
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });

        window.chrome = {
            runtime: {},
            loadTimes: function() {},
            csi: function() {},
            app: {},
        };
    """)

    return p, browser, context

async def run_scrape():
    p, browser, ctx = await create_stealth_browser()
    page = await ctx.new_page()
    
    try:
        try:
            await page.goto(INITIAL_URL)

            res = await intercept_api_call(page, TARGET_URL)

            with open('results/api_response.json', "w", encoding="utf-8") as f:
                json.dump(res, f, indent=2)
            
        finally:
            await page.close()
            await ctx.close()
    finally:
        await browser.close()
        await p.stop()

async def intercept_api_call(page, url):
    async with page.expect_response(lambda resp: "/api/v2/hotel/search/rooms" in resp.url and resp.request.method == "POST") as resp_info:
        await page.goto(url, wait_until="domcontentloaded")

    response = await resp_info.value
    return await response.json()