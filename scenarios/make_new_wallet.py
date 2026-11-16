import re
import time

import openai
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import JIRA_BOARD_URL
from reporting.telegram_chat import send_error_message


def make_new_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model):
    try:
        # Click "새 지갑 만들기"
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="새 지갑 생성"]').click()
        driver.implicitly_wait(30)

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

        # Mnemonic (Recovery Phrase) Generation and Entry
        targetText = '지갑 연결/복구에 사용할 비밀문구를 생성합니다.'
        element1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[contains(@name, "{targetText}")]'))
        )
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="비밀문구 확인"]').click()

        # Confirmation of Generated Mnemonic
        list_clip = [driver.find_element(By.XPATH,
                                         f'//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[{i + 1}]/XCUIElementTypeStaticText[2]').text
                     for i in range(12)]
        print("Nemonic =", list_clip)
        driver.find_element(By.XPATH,
                            '//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeButton[1]').click()
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="다음"]').click()
        strings = [driver.find_element(By.XPATH,
                                       f'//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText[{i}]').text
                   for i in range(1, 5)]
        answers = [list_clip[int(re.sub(r'[^0-9]', '', string)) - 1] for string in strings]
        for h in range(4):
            for j in range(4):
                for i in range(3):
                    word = driver.find_element(By.XPATH,
                                               f'//XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[{j + 1}]/XCUIElementTypeOther[2]/XCUIElementTypeOther[{i + 1}]/XCUIElementTypeButton')
                    if word.text == answers[h]:
                        word.click()
                        break
        driver.implicitly_wait(30)
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="다음"]').click()

        # Completion of Wallet Creation
        targetText = 'WEMIX 지갑 생성이 완료되었습니다.'
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[contains(@name, "{targetText}")]'))
        )
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="서비스 시작"]').click()
        driver.implicitly_wait(30)

        time.sleep(1)
        worksheet.update_acell("G10", "Pass")  # 새 지갑 생성 진행 완료
    except Exception as e:
        worksheet.update_acell("G10", "Fail")
        worksheet.update_acell('I10', f"Fail: {e}")
        testWork = worksheet.acell("D10").value
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
        worksheet.update_acell("J10", issue_link)
        quit()
