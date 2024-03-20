import sys
import os

from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, Playwright

from parser import parse_to_toml
from logger import log


UPV_LOGIN_URL = "https://intranet.upv.es/"
USERNAME = ""
PASSWORD = ""


def run(playwright: Playwright):

    if len(sys.argv) < 1:
        log("No output directory for the exams was provided", level="ERROR")
        exit(1)

    base_dir = os.path.abspath(sys.argv[1])

    # Create a new instance of chromium and open a new page
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()

    # Set a timeout of 10 seconds for each action
    page.set_default_timeout(10000)

    # Log in and navigate to the grades page
    login(page)
    goto_grades(page)

    # Parses each exam into a toml file
    parse_to_toml(page, base_dir)


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

    # Wait for the page to load
    page.wait_for_event("load")


def main():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()
