import asyncio
import os
import subprocess

from playwright.async_api import async_playwright
from playwright.async_api import Page, Playwright

from parser import parse_grades


UPV_LOGIN_URL = "https://intranet.upv.es/"
USERNAME = "20934366"
PASSWORD = "cuswiw-sukti0-hehbEv"
EXAM_FILES_PATH = "/Users/joan/Downloads/not/"


async def run(playwright: Playwright):
    # Create a new instance of chromium and open a new page
    chromium = playwright.chromium
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()

    # Set a timeout of 5 seconds for each action
    page.set_default_timeout(5000)

    # Log in and navigate to the grades page
    await login(page)
    await goto_grades(page)

    # Parse the grades
    exams = await parse_grades(page)

    # Create a file for all parsed exams
    [exam.create_file() for exam in exams]

    # Parse exams in the correct toml format
    for root, _, files in os.walk(EXAM_FILES_PATH):
        for file in files:
            subprocess.run(["parser", f"{root}/{file}"])


async def login(page: Page):
    # Go to the login page
    await page.goto(UPV_LOGIN_URL)

    # Fill the login form and submit it
    form = page.locator("form[name='alumno']")
    await form.locator("input[name='dni']").fill(USERNAME)
    await form.locator("input[name='clau']").fill(PASSWORD)
    await form.locator("input[type='submit']").click()


async def goto_grades(page: Page):
    # Enter intranet
    await page.locator("//div[@id='intranet']//a[2]").click()

    # Enter grades page
    await page.locator(
        "//div[@id='subgrupo_402']//table[@id='elemento_405']//a"
    ).click()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())
