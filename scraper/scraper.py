from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, Playwright

from parser import parse_exams
from logger import log


UPV_LOGIN_URL = "https://intranet.upv.es/"
USERNAME = "20934366"
PASSWORD = "cuswiw-sukti0-hehbEv"
EXAM_FILES_PATH = "/Users/joan/Downloads/not/"


def run(playwright: Playwright):
    # Create a new instance of chromium and open a new page
    chromium = playwright.chromium
    browser = chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    # Set a timeout of 5 seconds for each action
    page.set_default_timeout(15000)

    # Log in and navigate to the grades page
    login(page)
    goto_grades(page)

    # Parse the grades
    exams = parse_exams(page)

    log("\nDone!")


def login(page: Page):
    log("Logging in...")

    try:
        # Go to the login page
        page.goto(UPV_LOGIN_URL)

        # Fill the login form and submit it
        form = page.locator("form[name='alumno']")
        form.locator("input[name='dni']").fill(USERNAME)
        form.locator("input[name='clau']").fill(PASSWORD)
        form.locator("input[type='submit']").click()

        # Check if the login was successful
        assert page.title() == "Mi UPV"

    except AssertionError:
        log("Login failed. Please use a valid username and password.", level="ERROR")
        exit(1)


def goto_grades(page: Page):
    log("Navigating to grades page...")

    # Enter intranet
    page.locator("//div[@id='intranet']//a[2]").click()

    # Enter grades page
    page.locator("//div[@id='subgrupo_402']//table[@id='elemento_405']//a").click()


def main():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()
