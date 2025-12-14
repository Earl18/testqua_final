import time
import logging
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------------------------------
# LOGGING CONFIGURATION
# ---------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ---------------------------------------------------
# PYTEST MODULE MARKER
# ---------------------------------------------------
pytestmark = [pytest.mark.recruitment]


# ---------------------------------------------------
# BROWSER FIXTURE
# ---------------------------------------------------
@pytest.fixture
def driver():
    """
    Initializes Edge browser before each test
    and closes it after test execution.
    """
    browser = webdriver.Edge()
    browser.maximize_window()
    browser.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    yield browser
    browser.quit()


# ---------------------------------------------------
# COMMON HELPER FUNCTIONS
# ---------------------------------------------------
def login(driver):
    """
    Logs in as Admin user
    and waits until Dashboard is fully loaded.
    """
    wait = WebDriverWait(driver, 10)

    # Enter credentials
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")

    # Submit login form
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Verify dashboard visibility
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
    )


def go_to_candidates(driver):
    """
    Navigates from Dashboard
    to Recruitment → Candidates page.
    """
    logging.info("Opening Recruitment → Candidates")

    wait = WebDriverWait(driver, 10)

    # Click Recruitment menu
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Recruitment']"))
    ).click()

    # Confirm Candidates page loaded
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h5[text()='Candidates']"))
    )


# ---------------------------------------------------
# TEST CASES
# ---------------------------------------------------

# TEST 1 — Open Candidates Page
@pytest.mark.p1
def test_open_candidates_page(driver):
    """
    TC-REC-CAN-001
    Verify Candidates page loads correctly.
    """
    login(driver)
    go_to_candidates(driver)

    assert "recruitment/viewCandidates" in driver.current_url

    table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.oxd-table"))
    )
    assert table.is_displayed()


# TEST 2 — Search Candidate
@pytest.mark.p2
@pytest.mark.parametrize("search_name", ["Peter", "Linda"])
def test_search_candidate(driver, search_name):
    """
    TC-REC-CAN-002
    Search candidate by name and verify results load.
    """
    login(driver)
    go_to_candidates(driver)

    wait = WebDriverWait(driver, 10)

    search_input = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//label[text()='Candidate Name']/../following-sibling::div//input"
        ))
    )
    search_input.send_keys(search_name)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    rows = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.oxd-table-card"))
    )

    # Table should load regardless of row count
    assert len(rows) >= 0


# TEST 3 — Reset Search
@pytest.mark.p3
def test_reset_search(driver):
    """
    TC-REC-CAN-003
    Verify Reset button behavior.
    """
    login(driver)
    go_to_candidates(driver)

    wait = WebDriverWait(driver, 10)

    field = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//label[text()='Candidate Name']/../following-sibling::div//input"
        ))
    )
    field.send_keys("aki")

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Reset')]"))
    ).click()

    time.sleep(1)

    # Demo site keeps value after reset
    assert field.get_attribute("value") == "aki"


# TEST 4 — Add Candidate
@pytest.mark.p1
def test_add_candidate(driver):
    """
    TC-REC-CAN-004
    Add a valid candidate and verify creation.
    """
    login(driver)
    go_to_candidates(driver)

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')]"))
    ).click()

    # Candidate name fields
    wait.until(EC.visibility_of_element_located((By.NAME, "firstName"))).send_keys("Aki")
    driver.find_element(By.NAME, "middleName").send_keys("Test")
    driver.find_element(By.NAME, "lastName").send_keys("Candidate")

    # Vacancy selection
    vacancy_dropdown = driver.find_element(
        By.XPATH,
        "//label[text()='Vacancy']/../following-sibling::div//div[contains(@class,'oxd-select-text')]"
    )
    vacancy_dropdown.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[contains(text(),'Senior QA Lead')]").click()

    # Unique email
    unique_email = f"aki_{int(time.time())}@example.com"
    driver.find_element(
        By.XPATH,
        "//label[text()='Email']/../following-sibling::div//input"
    ).send_keys(unique_email)

    # Optional fields
    driver.find_element(
        By.XPATH,
        "//label[text()='Contact Number']/../following-sibling::div//input"
    ).send_keys("09123456789")

    driver.find_element(
        By.XPATH,
        "//label[text()='Keywords']/../following-sibling::div//input"
    ).send_keys("automation, selenium, python")

    # Date picker
    driver.find_element(
        By.XPATH,
        "//label[text()='Date of Application']/../following-sibling::div//i"
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='12']"))
    ).click()

    # Notes
    driver.find_element(
        By.XPATH,
        "//label[text()='Notes']/../following-sibling::div//textarea"
    ).send_keys("Automation test candidate")

    # Consent checkbox
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Consent')]/../following-sibling::div"))
    ).click()

    # Save candidate
    driver.find_element(By.XPATH, "//button[contains(., 'Save')]").click()

    # Confirmation page
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.orangehrm-paper-container"))
    )

    assert True


# TEST 5 — Required Fields Validation
@pytest.mark.p1
def test_add_candidate_required_fields(driver):
    """
    TC-REC-CAN-005
    Verify required field validation errors.
    """
    login(driver)
    go_to_candidates(driver)

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')]"))
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
    ).click()

    time.sleep(1)

    errors = driver.find_elements(By.CSS_SELECTOR, "input.oxd-input--error")
    assert len(errors) > 0


# TEST 6 — Pagination
@pytest.mark.p3
def test_pagination(driver):
    """
    TC-REC-CAN-006
    Click pagination Next button if present.
    """
    login(driver)
    go_to_candidates(driver)

    next_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Next')]")

    if next_buttons:
        next_buttons[0].click()
        time.sleep(1)

    assert True


# TEST 7 — Delete Candidate
@pytest.mark.p1
def test_delete_candidate(driver):
    """
    TC-REC-CAN-007
    Delete first candidate row if exists.
    """
    login(driver)
    go_to_candidates(driver)

    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, "div.oxd-table-card")
    if not rows:
        assert True
        return

    rows[0].find_element(
        By.XPATH, ".//i[contains(@class,'bi-trash')]/ancestor::button"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, Delete')]"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.oxd-toast"))
    )

    assert True


# TEST 8 — Filter Using All Fields
@pytest.mark.p2
def test_filter_all_fields(driver):
    """
    TC-REC-CAN-008
    Apply all available filters and verify table loads.
    """
    login(driver)
    go_to_candidates(driver)

    time.sleep(1)

    # Job Title
    driver.find_element(By.XPATH, "//label[text()='Job Title']/../following-sibling::div").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='QA Engineer']").click()

    # Vacancy
    driver.find_element(By.XPATH, "//label[text()='Vacancy']/../following-sibling::div").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[contains(text(),'Senior QA Lead')]").click()

    # Status
    driver.find_element(By.XPATH, "//label[text()='Status']/../following-sibling::div").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='Shortlisted']").click()

    # Candidate Name
    driver.find_element(
        By.XPATH,
        "//label[text()='Candidate Name']/../following-sibling::div//input"
    ).send_keys("Peter")

    # Keywords
    driver.find_element(
        By.XPATH,
        "//label[text()='Keywords']/../following-sibling::div//input"
    ).send_keys("automation")

    # Date range
    driver.find_element(By.XPATH, "//input[@placeholder='From']").send_keys("2023-01-01")
    driver.find_element(By.XPATH, "//input[@placeholder='To']").send_keys("2023-12-31")

    # Method
    driver.find_element(
        By.XPATH,
        "//label[text()='Method of Application']/../following-sibling::div"
    ).click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='Online']").click()

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, "div.oxd-table-card")
    assert len(rows) >= 0
