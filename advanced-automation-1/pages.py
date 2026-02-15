from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class InsiderPages:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    NAV_COMPANY = (By.XPATH, "//a[contains(.,'Company')]")
    FOOTER_CAREERS = (By.XPATH, "//a[@data-text=\"We're hiring\"]")
    CAREER_LOCATIONS = (By.XPATH, "//section[contains(@id, 'career-our-location')] | //h3[contains(text(), 'Our Locations')]")
    CAREER_TEAMS = (By.XPATH, "//section[contains(@id, 'career-find-our-calling')] | //h3[contains(text(), 'Find your calling')]")
    TEXT_OUR_LOCATIONS = (By.XPATH, "//*[contains(text(), 'Our locations')]")
    TEXT_LIFE_AT_INSIDER = (By.XPATH, "//*[contains(text(), 'Life at Insider')]")
    ACCEPT_COOKIES = (By.ID, "wt-cli-accept-all-btn")

    ALL_TEAMS_BUTTON = (By.XPATH, "//a[contains(text(), 'See all teams')]")
    QA_TEAM_CARD = (By.XPATH, "//h3[text()='Quality Assurance']")
    SEE_ALL_QA_JOBS = (By.LINK_TEXT, "See all QA jobs")
    SEE_ALL_TEAMS_BTN = (By.XPATH, "//a[contains(text(), 'See all teams')]")
    QA_JOBS_BUTTON = (By.XPATH, "//div[@data-department='Quality Assurance']//a")

    FILTER_LOCATION_BOX = (By.ID, "select2-filter-by-location-container")
    FILTER_DEPT_BOX = (By.ID, "select2-filter-by-department-container")
    JOB_POST_TITLE = (By.CLASS_NAME, "position-title")
    JOB_POST_DEPT = (By.CLASS_NAME, "position-department")
    JOB_POST_LOCATION = (By.CLASS_NAME, "position-location")
    VIEW_ROLE_BUTTON = (By.XPATH, "//a[contains(text(),'View Role')]")

    # --- METHODS ---
    def open_home(self):
        self.driver.get("https://useinsider.com/")
        try:
            self.wait.until(EC.element_to_be_clickable(self.ACCEPT_COOKIES)).click()
        except:
            pass

    def navigate_to_careers(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        careers_link = self.wait.until(EC.presence_of_element_located(self.FOOTER_CAREERS))

        self.driver.execute_script("arguments[0].click();", careers_link)

    def verify_careers_page(self):
        expected_url = "https://insiderone.com/careers/"
        self.wait.until(EC.url_to_be(expected_url))
        self.driver.execute_script("window.scrollTo(0, 1000);")
        try:
            locations_visible = self.wait.until(
                EC.visibility_of_element_located(self.TEXT_OUR_LOCATIONS)).is_displayed()
            life_visible = self.wait.until(EC.visibility_of_element_located(self.TEXT_LIFE_AT_INSIDER)).is_displayed()

            print("\n[INFO] URL ve Metinler doğrulandı.")
            return locations_visible and life_visible
        except Exception as e:
            print(f"\n[ERROR] Doğrulama başarısız: {e}")
            return False

    def filter_qa_jobs(self):
        import time
        all_teams_btn = self.wait.until(EC.presence_of_element_located(self.SEE_ALL_TEAMS_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_teams_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", all_teams_btn)

        print("\n[INFO] 'See all teams' tıklandı, QA kartı aranıyor...")
        time.sleep(3)

        qa_xpath = "//h3[contains(text(), 'Quality Assurance')]/ancestor::div[contains(@class, 'grid-item')]//a"
        qa_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, qa_xpath)))
        self.driver.execute_script("arguments[0].click();", qa_btn)
        print("[INFO] '6 Open Positions' butonuna tıklandı.")

        time.sleep(4)
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])
            print(f"[INFO] Yeni sekmeye geçildi: {self.driver.current_url}")


        self.wait.until(EC.url_contains("Quality"))


        time.sleep(5)


        location_dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'filter-button') and text()='Location']")))
        self.driver.execute_script("arguments[0].click();", location_dropdown)
        print("[INFO] Lever 'Location' kutusuna tıklandı.")

        time.sleep(1)
wait = WebDriverWait(self.driver, 20)

istanbul_option = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Istanbul')]"))
)

self.driver.execute_script("arguments[0].scrollIntoView(true);", istanbul_option)

wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Istanbul')]")))

istanbul_option.click()

        print("[INFO] Lever üzerinde Istanbul filtresi uygulandı.")
        time.sleep(5)

    def verify_job_list(self):
        import time
        time.sleep(3)

        try:
            job_postings = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "posting")))
        except:
            print("[ERROR] Hiç ilan bulunamadı!")
            return False

        print(f"\n[INFO] Toplam {len(job_postings)} ilan bulundu. Doğrulanıyor...")

        for job in job_postings:

            title = job.find_element(By.TAG_NAME, "h5").text
            details = job.find_elements(By.CLASS_NAME, "sort-by-location")
            all_job_text = job.text

            print(f"[CHECK] İlan Metni: {title} | Konum Bilgisi: {all_job_text.replace('\n', ' ')}")
            assert "Quality Assurance" in title or "QA" in title, f"Hatalı Pozisyon: {title}"
            assert "ISTANBUL" in all_job_text.upper(), f"Hatalı Konum: {all_job_text}"
            assert "QUALITY ASSURANCE" in all_job_text.upper() or "QA" in all_job_text.upper(), \
                f"Departman bilgisi bulunamadı: {all_job_text}"

        print("[INFO] Tüm ilanlar başarıyla doğrulandı.")
        return True

    def go_to_lever(self):
        import time
        job_item = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "posting")))
        apply_btn = job_item.find_element(By.XPATH, ".//a[contains(text(), 'Apply')]")

        print("\n[INFO] İlk ilanın 'Apply' butonuna tıklanıyor...")
        self.driver.execute_script("arguments[0].click();", apply_btn)
        time.sleep(5)
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])
            print(f"[INFO] Yeni sekmeye geçildi. Mevcut URL: {self.driver.current_url}")
        try:
            self.wait.until(lambda d: "lever" in d.current_url.lower())
            print(f"[SUCCESS] Başvuru sayfası başarıyla açıldı: {self.driver.current_url}")
        except Exception as e:
            print(f"[ERROR] URL doğrulanamadı. Mevcut URL: {self.driver.current_url}")
            raise e

        return True
