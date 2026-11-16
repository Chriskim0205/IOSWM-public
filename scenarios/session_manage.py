from selenium.webdriver.common.by import By


def session_manage(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model):
    driver.find_element(By.XPATH,
                        '//XCUIElementTypeTable/XCUIElementTypeCell[3]/XCUIElementTypeOther[1]/XCUIElementTypeOther').click()
    driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="icOutline24Back"]').click()
    worksheet.update_acell("G55", 'Not Test')  # 지갑 연결 세션 관리 > 연결 해제 동작 확인(위믹스 파이)
    worksheet.update_acell("G56", 'Not Test')  # 지갑 연결 세션 관리 > 연결 해제 동작 확인(Nile)
    worksheet.update_acell("G57", 'Not Test')  # 지갑 연결 세션 관리 > 연결 해제 동작 확인(Kurrency)

