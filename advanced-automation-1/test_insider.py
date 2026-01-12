from pages import InsiderPages


def test_insider_automation(driver):
    page = InsiderPages(driver)

    # 1. Ana sayfa erişimi
    page.open_home()
    assert "Insider" in driver.title

    # 2. Kariyer sayfası kontrolleri
    page.navigate_to_careers()
    assert page.verify_careers_page()

    # 3. QA Filtreleme
    page.filter_qa_jobs()

    # 4. İlan doğrulama
    page.verify_job_list()

    # 5. Lever sayfasına geçiş
    main_window = driver.current_window_handle
    page.go_to_lever()

    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            break

    assert "lever.co" in driver.current_url