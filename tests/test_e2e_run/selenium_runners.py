from selenium import webdriver
from selenium.webdriver.common.by import By


def run_csrf_form_submitsuccess(driver):
    # Step # | name | target | value
    # 1 | open | / |
    driver.get("http://127.0.0.1:5000/")
    # 2 | setWindowSize | 736x729 |
    driver.set_window_size(736, 729)
    # 3 | click | css=html |
    driver.find_element(By.CSS_SELECTOR, "html").click()
    # 4 | click | css=form |
    driver.find_element(By.CSS_SELECTOR, "form").click()
    # 5 | click | id=field2 |
    driver.find_element(By.ID, "field2").click()
    # 6 | click | id=field1 |
    driver.find_element(By.ID, "field1").click()
    # 7 | type | id=field1 | alpha
    driver.find_element(By.ID, "field1").send_keys("alpha")
    # 8 | type | id=field2 | beta
    driver.find_element(By.ID, "field2").send_keys("beta")
    # 9 | click | id=submit |
    driver.find_element(By.ID, "submit").click()


selenium_runs = {
    "http_apps/csrf_form": [run_csrf_form_submitsuccess],
}
