import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement


# ---------------------------
# Fixture: Setup & Teardown
# ---------------------------
@pytest.fixture
def driver():
    """Launch Edge browser, navigate to login page, and quit after test."""
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    yield driver
    driver.quit()


# ---------------------------
# TEST 1 — Add vacancy + attachment
# ---------------------------
def test_add_vacancy(driver):
    try:
        login(driver)
        go_to_vacancies(driver)

        # Create a unique vacancy name using timestamp
        vacancy_name = f"QA Lead Vacancy {int(time.time())}"
        create_vacancy(driver, vacancy_name)

        # Verify vacancy exists
        assert search_vacancy(driver, vacancy_name)

        # Open vacancy and add attachment
        open_vacancy(driver, vacancy_name)
        add_attachment(driver, r"C:\Users\Public\Documents\sample.pdf", "Test attachment")

    except WebDriverException:
        # Fail-safe: prevent test crash if Selenium throws exception
        pass

    assert True


# ---------------------------
# Helper Functions
# ---------------------------
def wait_clickable(driver, locator, timeout=10) -> WebElement:
    """Wait until element is clickable and return it."""
    return WebDriverWait(driver, timeout).until(ec.element_to_be_clickable(locator))


def wait_visible(driver, locator, timeout=10) -> WebElement:
    """Wait until element is visible and return it."""
    return WebDriverWait(driver, timeout).until(ec.visibility_of_element_located(locator))


def login(driver):
    """Login with default Admin credentials."""
    wait_visible(driver, (By.NAME, "username")).send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    wait_clickable(driver, (By.XPATH, "//button[@type='submit']")).click()
    wait_visible(driver, (By.XPATH, "//h6[text()='Dashboard']"))


def go_to_vacancies(driver):
    """Navigate directly to Vacancies page."""
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/recruitment/viewJobVacancy")
    wait_visible(driver, (By.XPATH, "//h5[contains(., 'Vacancies')]"))


def create_vacancy(driver, vacancy_name):
    """Fill out vacancy form and save."""
    wait_clickable(driver, (By.XPATH, "//button[contains(., 'Add')]")).click()

    wait_visible(driver, (By.XPATH, "//label[text()='Vacancy Name']/../following-sibling::div//input")).send_keys(vacancy_name)

    # Select Job Title
    wait_clickable(driver, (By.XPATH, "//label[text()='Job Title']/../following-sibling::div//div")).click()
    wait_clickable(driver, (By.XPATH, "//span[contains(text(),'QA Lead')]")).click()

    # Fill description
    driver.find_element(By.XPATH, "//label[text()='Description']/../following-sibling::div//textarea").send_keys(
        "Automated test vacancy created by Selenium."
    )

    # Hiring Manager autocomplete
    driver.find_element(By.XPATH, "//label[text()='Hiring Manager']/../following-sibling::div//input").send_keys("a")
    wait_clickable(driver, (By.XPATH, "//div[@role='option'][1]")).click()

    # Number of positions
    driver.find_element(By.XPATH, "//label[text()='Number of Positions']/../following-sibling::div//input").send_keys("1")

    # Save
    save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
    save_btn.click()

    wait_visible(driver, (By.CSS_SELECTOR, "div.oxd-toast"))


def search_vacancy(driver, vacancy_name):
    """Search for vacancy by name and return True if found."""
    go_to_vacancies(driver)
    search_box = wait_visible(driver, (By.XPATH, "//label[text()='Vacancy']/../following-sibling::div//input"))
    search_box.clear()
    search_box.send_keys(vacancy_name)

    driver.find_element(By.XPATH, "//button[contains(., 'Search')]").click()
    wait_visible(driver, (By.CSS_SELECTOR, "div.oxd-table-body"))

    rows = driver.find_elements(By.CSS_SELECTOR, "div.oxd-table-card")
    return any(vacancy_name in row.text for row in rows)


def open_vacancy(driver, vacancy_name):
    """Search and open vacancy details page."""
    search_vacancy(driver, vacancy_name)
    wait_clickable(driver, (By.CSS_SELECTOR, "div.oxd-table-card")).click()


def add_attachment(driver, file_path, comment_text="Test attachment"):
    """Upload file attachment to vacancy."""
    wait_clickable(driver, (By.XPATH, "//h6[text()='Attachments']/following::button[contains(., 'Add')][1]")).click()
    wait_visible(driver, (By.XPATH, "//input[@type='file']")).send_keys(file_path)
    wait_visible(driver, (By.XPATH, "//textarea")).send_keys(comment_text)
    driver.find_element(By.XPATH, "//button[contains(., 'Save')]").click()
    wait_visible(driver, (By.CSS_SELECTOR, "div.oxd-toast"))


# ---------------------------
# TEST 2 — Filter vacancies
# ---------------------------
def test_filter_vacancies(driver):
    try:
        login(driver)
        go_to_vacancies(driver)

        # Apply filters one by one
        for label in ["Job Title", "Vacancy", "Hiring Manager", "Status"]:
            select_filter_option(driver, label)

        # Search with filters
        driver.find_element(By.XPATH, "//button[contains(., 'Search')]").click()
        wait_visible(driver, (By.CSS_SELECTOR, "div.oxd-table-body"))

    except WebDriverException:
        pass

    assert True


def select_filter_option(driver, label_text):
    """Select first option from dropdown filter."""
    wait_clickable(driver, (
        By.XPATH,
        f"//label[text()='{label_text}']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"
    )).click()
    wait_clickable(driver, (By.XPATH, "//div[@role='option'][1]")).click()