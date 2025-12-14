# OrangeHRM Recruitment – Vacancies Automation (Selenium + Pytest)

## Overview
This repository contains automated functional tests for the **Vacancies module** in the OrangeHRM Recruitment system.  
It validates workflows such as navigation, vacancy creation, search, filtering, pagination, and attachment management on the demo site.

The goal is to:
- Ensure the Vacancies module behaves correctly across major workflows.
- Demonstrate stable Selenium automation using Python + Pytest.
- Provide reusable, maintainable test scripts.
- Produce clear documentation aligned with QA standards and rubric requirements.

---

## Tools & Technologies
- Python 3  
- Selenium WebDriver  
- Pytest  
- Microsoft Edge WebDriver  
- PyCharm IDE  

---

## Test Environment
- **URL:** https://opensource-demo.orangehrmlive.com  
- **Browser:** Microsoft Edge  
- **OS:** Windows 11  
- **Demo environment:** data resets periodically  

**Assumptions**
- The OrangeHRM demo site is available and functional.  
- Vacancy list and test data may vary over time.  
- Attachments are optional for the Add Vacancy scenario.  

**Constraints**
- Demo site performance may fluctuate.  
- No backend or database access.  
- Limited control over persistence of vacancy data (demo environment can reset).  

---

## Test Coverage

| Test Case ID | Description                | Priority |
|--------------|----------------------------|----------|
| TCRECVAC001  | Open Vacancies Page        | P1       |
| TCRECVAC002  | Search Vacancy             | P2       |
| TCRECVAC003  | Add Vacancy                | P1       |
| TCRECVAC004  | Required Fields Validation | P1       |
| TCRECVAC005  | Add Attachment to Vacancy  | P2       |
| TCRECVAC006  | Filter Vacancies           | P2       |
| TCRECVAC007  | Delete Vacancy             | P1       |
| TCRECVAC008  | Pagination                 | P3       |

---

## Choice of Scenarios
The **Add Vacancy scenario (TCRECVAC003)** is the most critical. It verifies that an HR user can:
- Open the Add Vacancy form.  
- Fill in all required fields with valid data.  
- Optionally upload an attachment.  
- Save the vacancy record.  
- See the new vacancy appear in the Vacancies list.  

Supporting scenarios (search, filter, delete, pagination) complete the coverage of how recruiters manage vacancies in the system.

---

## 🖥 Selenium WebDriver Implementation

### Correct Usage
- Driver initialization in a Pytest fixture.  
- Window maximization for consistent UI layout.  
- Explicit waits (`WebDriverWait + expected_conditions`).  
- Clean teardown via `driver.quit()`.  
- Accurate locators using labels, XPaths, and CSS selectors.  
- Handling of dynamic UI elements (dropdowns, autocomplete fields).  

### Stability & Reliability
- Non‑flaky tests by relying on explicit waits.  
- Unique timestamps for vacancy names to avoid collisions.  
- Validation of page redirects and table loads.  

### Best Practices
- Reusable helper functions: `login`, `go_to_vacancies`, `create_vacancy`, `search_vacancy`, `open_vacancy`, `add_attachment`, `select_filter_option`.  
- Modular test structure with one logical scenario per `test_*` function.  
- Clean locator strategy centered on visible labels.  
- Pytest fixtures for setup/teardown.  
- Consistent naming conventions for tests, helpers, and variables.  

---

## Pytest Framework Implementation

### Fixtures
- Central `driver()` fixture handles browser setup, navigation to login, and teardown.

### Structure & Organization
- Test files follow `test_*.py` naming.  
- Test functions are named `test_*` and contain assertions.  
- Markers (e.g., `@pytest.mark.p1`) can group tests by priority.  
- Tests are independent and reuse helper functions.  

### Execution & Parametrization
- Independent tests cover different vacancy workflows.  
- Helper functions reduce duplication.  
- Parametrization can be added later for multiple data sets or filter combinations.  

---

## Assertions, Reporting & Logging

### Assertions
- URL and page title confirm Vacancies page opened correctly.  
- Table visibility after navigation, search, or filtering.  
- Vacancy presence after adding and searching.  
- Required field errors when mandatory fields are left empty.  
- Pagination behavior when clicking Next/Previous.  

### Reporting Tools
- `pytest-html` for HTML reports.  
- Logging plugins for machine‑readable logs.  
- Screenshots on failure attached to reports.  

### Logging & Error Handling
- Python `logging` module integrated to log key steps:  
  - “Logging in as Admin”  
  - “Navigating to Vacancies page”  
  - “Adding vacancy: <name>”  
  - “Applying filters: Job Title, Vacancy, Status”  
  - “Deleting vacancy: <name>”  
- Try/except blocks catch WebDriver exceptions and log meaningful error messages.  

---

## Running Tests

- **Basic run (all tests):**
  ```bash
  pytest -v
