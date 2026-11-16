import openai
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import JIRA_BOARD_URL, WALLET_SECOND_PRIVATE_KEY
from reporting.telegram_chat import send_error_message


def setting_load_walet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model):
    targetText = "자산 관리 목적에 따라 여러 개의 지갑을 추가하여 용도별로 관리할 수 있습니다."
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[contains(@name, "{targetText}")]'))
        )
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="icOutline24Add"]').click()
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="다른 지갑 불러오기"]').click()
        AOS_Second_PrivateKey = WALLET_SECOND_PRIVATE_KEY
        driver.find_element(By.XPATH, '//XCUIElementTypeTextView[@value="프라이빗 키 입력"]').send_keys(AOS_Second_PrivateKey)
        driver.find_element(By.XPATH, '//XCUIElementTypeStaticText[@name="불러올 WEMIX 지갑의 프라이빗 키를 입력하세요."]').click()
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="다음"]').click()
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="완료"]').click()

        worksheet.update_acell("G51", "Pass")  # 지갑 관리  > 다른 지갑 불러오기 진행 완료
    except Exception as e:
        worksheet.update_acell("G51", "Fail")
        worksheet.update_acell('I51', f"Fail: {e}")
        testWork = worksheet.acell("D51").value
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
        worksheet.update_acell("J51", issue_link)
        pass
