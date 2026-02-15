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

    # --- METHODS --- (after)

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

        # 1. See all teams butonu
        all_teams_btn = self.wait.until(
            EC.presence_of_element_located(self.SEE_ALL_TEAMS_BTN)
        )
        # Scroll ve Click işlemlerini JS ile yaparak stabiliteyi sağlıyoruz
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_teams_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", all_teams_btn)

        # Takımların yüklenmesi için bekleme süresini biraz artırdık
        time.sleep(5)

        # 2. QA team button
        qa_xpath = "//h3[contains(text(), 'Quality Assurance')]/ancestor::div[contains(@class, 'grid-item')]//a"

        # Butonun tıklanabilir olduğundan emin oluyoruz
        qa_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, qa_xpath)))
        self.driver.execute_script("arguments[0].click();", qa_btn)

        # 3. Sekme Geçişi ve URL Kontrolü (Hata Aldığın Yer)
        # Jenkins'te sekme açılması bazen 5-6 saniye sürebilir
        time.sleep(6)
        handles = self.driver.window_handles

        if len(handles) > 1:
            self.driver.switch_to.window(handles[-1])
            print(f"[INFO] Yeni sekmeye geçildi: {self.driver.current_url}")

        # URL kontrolünü biraz daha esnek yapıyoruz
        self.wait.until(lambda d: "Quality" in d.current_url or "lever" in d.current_url)

        # 4. Location filter
        # Lever sayfasında bazen elementler geç render olur, süreyi artırdık
        time.sleep(5)

        # 'Location' kutusunu bul ve tıkla
        location_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//span[contains(@id, 'select2-filter-by-location-container')] | //div[contains(@class, 'filter-button') and text()='Location']"))
        )
        self.driver.execute_script("arguments[0].click();", location_dropdown)

        # 5. Istanbul Seçimi
        # 'Istanbul, Turkey' tam metnini veya 'Istanbul'u içeren herhangi bir elementi yakalıyoruz
        istanbul_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(text(), 'Istanbul')] | //a[contains(text(), 'Istanbul')]"))
        )
        # Bazı durumlarda .click() yerine JS click daha garantidir
        self.driver.execute_script("arguments[0].click();", istanbul_option)

        print("[INFO] Istanbul filtresi uygulandı.")
        time.sleep(5)  # İlanların listelenmesi için bekleme

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
