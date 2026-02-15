from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InsiderPages:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    # --- LOCATORS ---
    FOOTER_CAREERS = (By.XPATH, "//a[@data-text=\"We're hiring\"]")
    TEXT_OUR_LOCATIONS = (By.XPATH, "//*[contains(text(), 'Our locations')]")
    TEXT_LIFE_AT_INSIDER = (By.XPATH, "//*[contains(text(), 'Life at Insider')]")
    ACCEPT_COOKIES = (By.ID, "wt-cli-accept-all-btn")

    SEE_ALL_TEAMS_BTN = (By.XPATH, "//a[contains(text(), 'See all teams')]")

    # --- METHODS ---

    def open_home(self):
        self.driver.get("https://useinsider.com/")
        try:
            self.wait.until(
                EC.element_to_be_clickable(self.ACCEPT_COOKIES)
            ).click()
        except Exception:
            pass

    def navigate_to_careers(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        careers_link = self.wait.until(
            EC.presence_of_element_located(self.FOOTER_CAREERS)
        )
        self.driver.execute_script("arguments[0].click();", careers_link)

    def verify_careers_page(self):
        expected_url = "https://insiderone.com/careers/"
        self.wait.until(EC.url_to_be(expected_url))

        self.driver.execute_script("window.scrollTo(0, 1000);")

        try:
            locations_visible = self.wait.until(
                EC.visibility_of_element_located(self.TEXT_OUR_LOCATIONS)
            ).is_displayed()

            life_visible = self.wait.until(
                EC.visibility_of_element_located(self.TEXT_LIFE_AT_INSIDER)
            ).is_displayed()

            return locations_visible and life_visible

        except Exception:
            return False

    def filter_qa_jobs(self):
        import time

        # See all teams
        all_teams_btn = self.wait.until(
            EC.presence_of_element_located(self.SEE_ALL_TEAMS_BTN)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            all_teams_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            all_teams_btn
        )

        time.sleep(3)

        # QA team button
        qa_xpath = (
            "//h3[contains(text(), 'Quality Assurance')]"
            "/ancestor::div[contains(@class, 'grid-item')]//a"
        )

        qa_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, qa_xpath))
        )
        self.driver.execute_script("arguments[0].click();", qa_btn)

        time.sleep(4)

        # Switch new tab if exists
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])

        self.wait.until(EC.url_contains("Quality"))

        # Location filter
        location_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'filter-button') and text()='Location']")
            )
        )
        self.driver.execute_script(
            "arguments[0].click();",
            location_dropdown
        )

        time.sleep(1)

        istanbul_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'Istanbul')] | //div[contains(text(), 'Istanbul')]")
            )
        )
        istanbul_option.click()

        time.sleep(4)

    def verify_job_list(self):
        try:
            job_postings = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "posting")
                )
            )
        except Exception:
            return False

        for job in job_postings:
            title = job.find_element(By.TAG_NAME, "h5").text
            all_job_text = job.text.upper()

            assert (
                "QUALITY ASSURANCE" in title.upper()
                or "QA" in title.upper()
            ), f"Hatalı Pozisyon: {title}"

            assert "ISTANBUL" in all_job_text, \
                f"Hatalı Konum: {all_job_text}"

            assert (
                "QUALITY ASSURANCE" in all_job_text
                or "QA" in all_job_text
            ), f"Departman bilgisi bulunamadı: {all_job_text}"

        return True

    def go_to_lever(self):
        import time

        job_item = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "posting")
            )
        )

        apply_btn = job_item.find_element(
            By.XPATH,
            ".//a[contains(text(), 'Apply')]"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            apply_btn
        )

        time.sleep(5)

        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])

        self.wait.until(
            lambda d: "lever" in d.current_url.lower()
        )

        return True
