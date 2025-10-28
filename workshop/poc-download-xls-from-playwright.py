import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        await page.goto("https://github.com/Desvart/auto-qsnap/blob/master/data/2025-metrics-tiny.xlsx")
        print(await page.title())
        async with page.expect_download() as download_info:
            # Perform the action that initiates download
            await page.get_by_test_id("download-raw-button").click()
        download = await download_info.value

        # Wait for the download process to complete and save the downloaded file somewhere
        await download.save_as("." + download.suggested_filename)
        await browser.close()

asyncio.run(main())