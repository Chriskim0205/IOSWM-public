import openai
from selenium.webdriver.common.by import By

from config import JIRA_BOARD_URL
from reporting.telegram_chat import send_error_message


def disconnect_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model):
    try:
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="icOutline24Setting"]').click()
        driver.find_element(By.XPATH,
                            '//XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther').click()
        driver.find_element(By.XPATH,
                            '//XCUIElementTypeTable/XCUIElementTypeCell[5]/XCUIElementTypeOther[1]/XCUIElementTypeOther').click()
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="지갑 삭제"]').click()
        for i in range(3):
            for j in range(2):
                driver.find_element(By.XPATH, f'//XCUIElementTypeStaticText[@name="{i + 1}"]').click()
        driver.implicitly_wait(30)

        worksheet.update_acell("G48", "Pass")  # 보안 설정 > 지갑 연결 해제 진행 완료
    except Exception as e:
        worksheet.update_acell("G48", "Fail")
        worksheet.update_acell('I48', f"Fail: {e}")
        testWork = worksheet.acell("D48").value
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
        worksheet.update_acell("J48", issue_link)
        quit()
