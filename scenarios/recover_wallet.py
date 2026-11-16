import time

import openai
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import JIRA_BOARD_URL, WALLET_MNEMONIC
from reporting.telegram_chat import send_error_message


def recover_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model):
    targetTextList = [
        'WEMIX 지갑은 가장 안전하고 투명한 지갑입니다.',
        '생태계의 다양한 토큰들을 관리하고, WEMIX와 WEMIX$를 쉽게 교환하세요.',
        '매력적인 NFT 작품들을 나만의 공간에 모으고, 한눈에 감상하세요.',
        'WEMIX 생태계의 다양한 서비스 경험을 함께해요.'
    ]
    try:
        # Iterate through the targetTextList
        for i, targetText in enumerate(targetTextList, start=1):
            element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
            expected_result = element.text
            if expected_result == targetText:
                driver.find_element(By.XPATH, '//XCUIElementTypeStaticText[@name="다음"]').click()
                driver.implicitly_wait(30)

        # Check '서비스 약관'
        targetText = '서비스 약관'
        element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
        location = element.location
        new_x, new_y = location['x'] + 10, location['y'] + 5
        TouchAction(driver).tap(x=new_x, y=new_y).perform()
        driver.implicitly_wait(30)
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="icOutline24Close"]').click()

        # Click CheckBox
        driver.find_element(By.XPATH,
                            '//XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeButton[1]').click()
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="기존 지갑 복구하기"]').click()
        driver.implicitly_wait(30)

        # Entet RestoreCode
        restore_code = WALLET_MNEMONIC
        targetText = "비밀문구를 입력하세요."
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[contains(@name, "{targetText}")]'))
        )
        driver.find_element(By.XPATH, '//XCUIElementTypeTextView[@value="비밀문구 입력"]').send_keys(restore_code)
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="다음"]').click()
        time.sleep(10)
        # Select Multi-Wallet
        driver.swipe(470, 1400, 470, 100, 700)  # scroll
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="다음"]').click()

        # Password Generation
        for _ in range(2):
            for i in range(3):
                for j in range(2):
                    driver.find_element(By.XPATH, f'//XCUIElementTypeStaticText[@name="{i + 1}"]').click()
        driver.implicitly_wait(30)

        # Face ID Configuration
        targetText = '비밀번호 등록이 완료되었습니다. Face ID도 사용하시겠습니까?'
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[contains(@name, "{targetText}")]'))
        )
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="사용 안 함"]').click()

        # Completion of Wallet Recover
        targetText = 'WEMIX 지갑 복구가 완료되었습니다.'
        element1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[contains(@name, "{targetText}")]'))
        )
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="서비스 시작"]').click()
        driver.implicitly_wait(30)

        worksheet.update_acell("G11", "Pass")  # 기존 지갑 복구하기 진행 완료
    except Exception as e:
        worksheet.update_acell("G11", "Fail")
        worksheet.update_acell('I11', f"Fail: {e}")
        testWork = worksheet.acell("D11").value
        question = f"{e}에서 message 문구를 해당 영역 코드에 맞게 {testWork}테스트 중 알아보기 쉽게 message를 사전 조건, 테스트 절차, 실제 결과, 기대 결과, 해결 방안을 절차에 따라 나눠서 상세하게 정리"
        completion = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}]
        )
        answer = completion.choices[0].message.content
        issue_dict = {
            'project': {'key': project_key},  # 프로젝트 키
            'summary': f'{testWork} 테스트 오류',  # 이슈 제목
            'description': f'{answer}',  # 이슈 설명
            'issuetype': {'name': issue_type},  # 이슈 타입 (Bug)
            "assignee": {"accountId": assign_list},  # 담당자 지정
            "labels": [label_list]  # 여기에 레이블 추가
        }
        new_issue = jira.create_issue(fields=issue_dict)
        issue_link = f"{JIRA_BOARD_URL}?selectedIssue={new_issue.key}"
        loop.run_until_complete(send_error_message(testWork, issue_link))
        worksheet.update_acell("J11", issue_link)
        quit()
