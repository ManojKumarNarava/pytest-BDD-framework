# Playwright Python BDD Automation Framework

A scalable, enterprise-grade UI automation framework built using **Python**, **Playwright**, **Pytest**, and **Pytest-BDD** following the **Page Object Model (POM)** design pattern.

This framework is designed for maintainability, readability, and easy integration into enterprise CI/CD pipelines.

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Playwright | Browser Automation |
| Pytest | Test Runner |
| Pytest-BDD | Behavior Driven Development |
| Page Object Model | UI Design Pattern |
| Allure Report | Interactive Test Reporting |
| Pytest HTML | HTML Test Report |
| Logging | Execution Logs |
| JSON | Test Data Management |
| Git & GitHub | Version Control |

---

# Features Implemented

## Test Automation

- Playwright browser automation
- Pytest test runner
- Pytest-BDD support
- Feature files
- Step Definitions
- Page Object Model (POM)

---

## Browser Management

Supports multiple browsers:

- Chromium
- Firefox
- WebKit

Centralized browser creation using Browser Manager.

---

## Configuration Management

Framework configuration is externalized using configuration files.

Examples include:

- Browser
- Base URL
- Timeouts
- Other execution settings

No hard-coded configuration inside test scripts.

---

## Test Data Management

JSON-based data reader supports external test data.

Example:

```json
{
  "search_text": "Playwright"
}
```

---

## Logging

Centralized logging utility provides:

- Test execution logs
- Error logging
- Debug logging
- Timestamped messages

---

## Assertions

Reusable custom assertion methods improve readability and reduce duplication.

Example:

```python
Assertions.assert_title(page, "Google")
```

---

## Screenshot on Failure

Whenever a test fails:

- Screenshot is automatically captured
- Saved under:

```
screenshots/
```

Screenshot capture occurs before browser teardown ensuring successful artifact collection.

---

# Reporting

## HTML Report

Framework generates a self-contained HTML report using:

```
pytest-html
```

Report location:

```
reports/test_report.html
```

Contains:

- Test summary
- Pass/Fail statistics
- Execution duration
- Failure details

---

## Allure Report

Interactive reporting using:

```
allure-pytest
```

Supports:

- Test steps
- Attachments
- Screenshots
- Execution history
- Categories
- Environment information

Generate results:

```bash
python -m pytest --alluredir=allure-results
```

View report:

```bash
allure serve allure-results
```

---

## Playwright Trace

Optional trace recording.

Execution:

```bash
python -m pytest --playwright-trace
```

Failed test traces are stored inside:

```
traces/
```

---

## Video Recording

Optional execution video recording.

Execution:

```bash
python -m pytest --record-video
```

Videos are stored inside:

```
videos/
```

---

# Project Design

The framework follows the Page Object Model.

```
Feature File
      ↓
Step Definition
      ↓
Page Object
      ↓
Playwright
```

Benefits:

- Reusable code
- Easy maintenance
- Separation of concerns
- Better scalability

---

# Utilities

The framework includes reusable utilities for:

- Browser Manager
- Config Reader
- Data Reader
- Logger
- Assertions

These utilities minimize duplicated code throughout the framework.

---

# Running Tests

Run all tests

```bash
python -m pytest
```

Run in headed mode

```bash
python -m pytest --headed
```

Run in headless mode

```bash
python -m pytest --headless
```

Generate HTML report

```bash
python -m pytest
```

Generate Allure report

```bash
python -m pytest --alluredir=allure-results
```

Open Allure report

```bash
allure serve allure-results
```

Record Playwright Trace

```bash
python -m pytest --playwright-trace
```

Record Video

```bash
python -m pytest --record-video
```

---

# Current Framework Capabilities

✔ Page Object Model

✔ Playwright Automation

✔ Pytest

✔ Pytest-BDD

✔ Browser Manager

✔ Configuration Reader

✔ JSON Data Reader

✔ Logger

✔ Custom Assertions

✔ Screenshot on Failure

✔ HTML Reporting

✔ Allure Reporting

✔ Playwright Trace Recording

✔ Video Recording

✔ Chromium Support

✔ Firefox Support

✔ WebKit Support

---

# Prerequisites

- Python 3.12+
- Git
- Playwright
- Java JDK 17+
- Allure Commandline

Install dependencies

```bash
pip install -r requirements.txt
```

Install Playwright browsers

```bash
python -m playwright install
```

---


# Author

**Manoj Kumar Narava**

Automation Test Analyst

Python • Playwright • Pytest • Pytest-BDD • Selenium • REST API • CI/CD • Banking Domain