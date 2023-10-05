from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    # Input login credentials
    username = input("Username: ")
    password = getpass("Password: ")

    # Create a new instance of the Safari web driver
    driver = webdriver.Safari()

    # Define implicit wait
    driver_wait = WebDriverWait(driver, 10)

    # Login and navigate to grades page
    login(driver, username, password)
    navigate_to_grades_page(driver_wait)


def login(driver, username, password):
    # Go to the login page
    driver.get("https://intranet.upv.es")

    # Login
    form = driver.find_element(By.XPATH, "//form[@name='alumno']")
    form.find_element(By.XPATH, "//input[@name='dni']").send_keys(username)
    form.find_element(By.XPATH, "//input[@name='clau']").send_keys(password)
    form.find_element(By.XPATH, "//input[@class='upv_btsubmit']").click()


def navigate_to_grades_page(driver_wait):
    # Enter intranet
    driver_wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='intranet']//a[2]"))
    ).click()

    # Enter grades page
    driver_wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='subgrupo_402']//table[@id='elemento_405']//a")
        )
    ).click()


if __name__ == "__main__":
    main()
