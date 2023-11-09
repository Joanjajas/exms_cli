import asyncio
import sys
import os

# from getpass import getpass

from playwright.async_api import Locator, async_playwright
from playwright.async_api import Page, Playwright


UPV_LOGIN_URL = "https://intranet.upv.es/"
USERNAME = "20934366"
PASSWORD = "cuswiw-sukti0-hehbEv"


async def run(playwright: Playwright):
    # Create a new instance of chromium and open a new page
    chromium = playwright.chromium
    browser = await chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()
    # browser context

    # Set a timeout of 5 seconds for each action
    page.set_default_timeout(5000)

    # Log in and navigate to the grades page
    await login(page)
    await goto_grades(page)
    await get_grades(page)

    print("Script finished successfully")


# NOTE: This function uses xpath to locate elements. Although this is not a good practice,
# the intranet page is a mess and it is the only way to consistently get the wanted elements
async def goto_grades(page: Page):
    print("Navigating to grades page...")

    try:
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


async def login(page: Page):
    # Input login credentials
    # username = input("Username: ")
    # password = getpass("Password: ")

    print("Logging in...")

    try:
        # Go to the login page
        await page.goto(UPV_LOGIN_URL)

        # Fill the login form and submit it
        form = page.locator("form[name='alumno']")
        await form.locator("input[name='dni']").fill(USERNAME)
        await form.locator("input[name='clau']").fill(PASSWORD)
        await form.locator("input[type='submit']").click()

        # Check if the login was succesfull
        assert await page.title() == "Mi UPV"

    except AssertionError:
        print(
            "Login failed. Make sure to use a valid username and password.",
            file=sys.stderr,
        )
        exit(1)

    except Exception as err:
        print(f"Error ocurred while logging in: {err}", file=sys.stderr)
        exit(1)


async def get_grades(page: Page):
    # await page.get_by_label("Todos").check()
    # await page.get_by_role("button", name="Consultar").click()

    table = page.locator("//div[@class='container'][4]")
    rows = table.locator("//tr")

    # Wait for the table to load
    await page.wait_for_event("load")

    subject_name = ""
    for row in await rows.all():
        if await row.locator("//td").count() == 1:
            subject_name = await row.text_content()

            if not os.path.exists(f"/Users/joan/Downloads/not/{subject_name}"):
                os.mkdir(f"/Users/joan/Downloads/not/{subject_name}")

        if await row.locator("//td").count() == 4:
            exam_info = row.locator("//td")
            exam_name = await exam_info.nth(2).text_content()
            await exam_info.nth(3).click()
            await inside_grades(page, subject_name, exam_name)


async def inside_grades(page: Page, subject_name, exam_name):
    await page.wait_for_event("load")

    table = page.locator("//table[@class='upv_listacolumnas']//tbody")

    names = await table.locator("//td[1]").all()
    grades = await table.locator("//td[2]").all()

    with open(f"/Users/joan/Downloads/not/{subject_name}/{exam_name}", "w") as f:
        for name, grade in zip(names, grades):
            f.write(f"{await name.text_content()} {await grade.text_content()}\n")

    await page.go_back()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())
