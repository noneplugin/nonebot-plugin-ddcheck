from contextlib import asynccontextmanager
from playwright.async_api import async_playwright
from os import getcwd

_browser = None
_playwright = None

async def init(**kwargs):
    global _browser
    global _playwright
    _playwright = await async_playwright().start()
    try:
        _browser = await launch_browser(**kwargs)
    except:
        await install_browser()
        _browser = await launch_browser(**kwargs)
    return _browser

async def launch_browser(**kwargs):
    assert _playwright is not None, "Playwright is not initialized"
    return await _playwright.chromium.launch(**kwargs)

async def get_browser(**kwargs):
    return _browser or await init(**kwargs)

@asynccontextmanager
async def get_new_page(**kwargs): 
    browser = await get_browser()
    page = await browser.new_page(**kwargs)
    try:
        yield page
    finally:
       await page.close()

async def shutdown_browser():
    if _browser:
       await _browser.close()
    if _playwright:
       await _playwright.stop() 

async def install_browser():
    import sys

    from playwright.__main__ import main

    sys.argv = ["", "install", "chromium"]
    try:
        main()
    except SystemExit:
        pass

async def html_to_pic(html="",wait: int = 10,**kwargs):
    async with get_new_page(**kwargs) as page:
        await page.goto(f"file://{getcwd()}")
        #await page.goto("http://bilibili.com")
        #await page.screenshot(path="a.png",full_page=True)
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(wait)
        img_raw = await page.screenshot(full_page=True)
        
    return img_raw
    
#我测试用的代码
"""import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(html_to_pic())


import jinja2
import asyncio

async def a():
    await html_to_pic("神仙捡破烂")

loop = asyncio.get_event_loop()
loop.run_until_complete( a())

"""
