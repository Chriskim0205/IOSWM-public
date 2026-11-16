import time

import openai
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import JIRA_BOARD_URL


def remove_install():
    try:
        driver.remove_app('com.wemixfoundation.wemixwallet')

        targetText = 'TestFlight'
        element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
        location = element.location
        new_x, new_y = location['x'] + 30, location['y'] + 50
        TouchAction(driver).tap(x=new_x, y=new_y).perform()
        driver.implicitly_wait(180)

        targetText = '설치'
        element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
        location = element.location
        new_x, new_y = location['x'], location['y']
        TouchAction(driver).tap(x=new_x, y=new_y).perform()
        driver.implicitly_wait(180)

        targetText = '열기'
        element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
        location = element.location
        new_x, new_y = location['x'], location['y']
        TouchAction(driver).tap(x=new_x, y=new_y).perform()
        time.sleep(5)

        targetText = '다음'
        element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
        location = element.location
        new_x, new_y = location['x'], location['y']
        TouchAction(driver).tap(x=new_x, y=new_y).perform()

        targetText = '테스트 시작'
        element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
        location = element.location
        new_x, new_y = location['x'], location['y']
        TouchAction(driver).tap(x=new_x, y=new_y).perform()
        driver.implicitly_wait(180)

        worksheet.update_acell("G7", "Pass")  # APP 삭제 후 새로 설치
    except Exception as e:
        worksheet.update_acell("G7", "Fail")
        worksheet.update_acell('I7', f"Fail: {e}")
        testWork = worksheet.acell("D7").value
        question = f"{e}에서 message 문구를 해당 영역 코드에 맞게 {testWork}테스트 중 알아보기 쉽게 message를 사전 조건, 테스트 절차, 실제 결과, 기대 결과, 해결 방안을 절차에 따라 나눠서 상세하게 정리"
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
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
        worksheet.update_acell("J7", f"{JIRA_BOARD_URL}?selectedIssue={new_issue.key}")
        quit()
