import asyncio
import sys
from getpass import getpass

from playwright.async_api import async_playwright


UPV_LOGIN_URL = "https://intranet.upv.es/"


async def run(playwright):
    # Create a new instance of chromium and open a new page
    chromium = playwright.chromium
    browser = await chromium.launch()
    page = await browser.new_page()

    # Set a timeout of 5 seconds for each action
    page.set_default_timeout(5000)

    # Log in and navigate to the grades page
    await goto_grades(page)
    await login(page)

    print("Script finished successfully")


# NOTE: This function uses xpath to locate elements. Although this is not a good practice,
# the intranet page is a mess and it is the only way to consistently get the wanted elements
async def goto_grades(page):
    try:
        # Log in
        print("Navigating to grades page...")

        # Enter intranet
        await page.locator("//div[@id='intranet']//a[2]").click()

        # Enter grades page
        await page.locator(
            "//div[@id='subgrupo_402']//table[@id='elemento_405']//a"
        ).click()

        # Check if we are in the grades page
        assert await page.title() == "UPV - Menú Intranet"

    except Exception as err:
        print(f"Error ocurred while navigating to grades: {err}", file=sys.stderr)
        exit(1)


async def login(page):
    # Input login credentials
    username = input("Username: ")
    password = getpass("Password: ")

    print("Logging in...")

    try:
        # Go to the login page
        await page.goto(UPV_LOGIN_URL)

        # Fill the login form and submit it
        form = page.locator("form[name='alumno']")
        await form.locator("input[name='dni']").fill(username)
        await form.locator("input[name='clau']").fill(password)
        await form.locator("input[type='submit']").click()

        # Check if the login was succesfull
        assert await page.title() == "Mi UPV"

    except AssertionError:
        print(
            "Login failed. Make sure to use a valid username and password.",
            file=sys.stderr,
        )
        exit(1)


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())
