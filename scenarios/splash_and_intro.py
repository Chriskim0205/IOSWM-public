import time

import openai
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import JIRA_SERVER
from reporting.telegram_chat import send_error_message


def splash_and_intro(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model):
    try:
        targetTextList = [
            'WEMIX 지갑은 가장 안전하고 투명한 지갑입니다.',
            '생태계의 다양한 토큰들을 관리하고, WEMIX와 WEMIX$를 쉽게 교환하세요.',
            '매력적인 NFT 작품들을 나만의 공간에 모으고, 한눈에 감상하세요.',
            'WEMIX 생태계의 다양한 서비스 경험을 함께해요.'
        ]
        # Iterate through the targetTextList
        for i, targetText in enumerate(targetTextList, start=1):
            element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
            expected_result = element.text
            if expected_result == targetText:
                # Move to the next page
                driver.find_element(By.XPATH, '//XCUIElementTypeStaticText[@name="다음"]').click()
                driver.implicitly_wait(30)

        # Check '서비스 약관'
        service = '서비스 약관'
        element_locator1 = (By.XPATH, f'//*[contains(@name, "{service}")]')
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator1))
        location = element.location
        new_x, new_y = location['x'] + 10, location['y'] + 5
        TouchAction(driver).tap(x=new_x, y=new_y).perform()
        driver.implicitly_wait(30)
        driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="icOutline24Close"]').click()

        # Click CheckBox
        driver.find_element(By.XPATH,
                            '//XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeButton[1]').click()

        # Update cell in the worksheet based on the result
        time.sleep(1)
        worksheet.update_acell('G9', 'Pass')  # Splash & Intro 화면 확인

    except Exception as e:
        worksheet.update_acell('G9', 'Fail')
        worksheet.update_acell('I9', f"Fail: {e}")

        testWork = worksheet.acell("D9").value
        question = f"{e}에서 message 문구를 해당 영역 코드에 맞게 {testWork}테스트 중 알아보기 쉽게 message를 사전 조건, 테스트 절차, 실제 결과, 기대 결과, 해결 방안을 절차에 따라 나눠서 상세하게 정리"
        completion = openai.chat.completions.create(
            model=model,
            messages=[{"role": "assistant", "content": question}]
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
        issue_link = f"{JIRA_SERVER}/browse/{new_issue.key}"
        loop.run_until_complete(send_error_message(testWork, issue_link))
        worksheet.update_acell("J9", issue_link)
        quit()

# def splash(driver, model, project_key, issue_type, assign_list, label_list, jira, loop):
#     global targetText, expected_result
#     try:
#         targetTextList = [
#             'WEMIX 지갑은 가장 안전하고 투명한 지갑입니다.',
#             '생태계의 다양한 토큰들을 관리하고, WEMIX와 WEMIX$를 쉽게 교환하세요.',
#             '매력적인 NFT 작품들을 나만의 공간에 모으고, 한눈에 감상하세요1.',
#             'WEMIX 생태계의 다양한 서비스 경험을 함께해요.'
#         ]
#         # Iterate through the targetTextList
#         for i, targetText in enumerate(targetTextList, start=1):
#             element_locator = (By.XPATH, f'//*[contains(@name, "{targetText}")]')
#             element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator))
#             expected_result = element.text
#             if expected_result == targetText:
#                 # Move to the next page
#                 driver.find_element(By.XPATH, '//XCUIElementTypeStaticText[@name="다음"]').click()
#                 driver.implicitly_wait(30)
#     except:
#         testWork ='Splash'
#         question = (f'너는 이제부터 QA 엔지니어야. {targetText}와 {expected_result} 문구가 상이하다는걸 발견했어. 형식은 사전조건, 테스트 절차, 실제 결과, 기대 결과로 나누어서 작성해야해.'
#                     f'사전조건에는 WEMIX WALLET 앱 설치 및 실행 문구 기입,'
#                     f'테스트 절차에는 ,'
#                     f'실제 결과에는 {targetText} 문구를 출력,'
#                     f' 기대 결과에는 {expected_result} 문구를 출력하고 ]['[무슨 문구가 다른지 작성.')
#         completion = openai.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": question}]
#         )
#         answer = completion.choices[0].message.content
#
#         issue_dict = {
#             'project': {'key': project_key},  # 프로젝트 키
#             'summary': 'Spalsh 화면 테스트 오류',  # 이슈 제목
#             'description': f'{answer}',  # 이슈 설명
#             'issuetype': {'name': issue_type},  # 이슈 타입 (Bug)
#             "assignee": {"accountId": assign_list},  # 담당자 지정
#             "labels": [label_list]  # 여기에 레이블 추가
#         }
#         new_issue = jira.create_issue(fields=issue_dict)
#         issue_link = f"{JIRA_SERVER}/browse/{new_issue.key}"
#         loop.run_until_complete(send_error_message(testWork, issue_link))
#         quit()
#
# def service(driver, model, project_key, issue_type, assign_list, label_list, jira, loop):
#     try:
#         service = '서비스 약관'
#         element_locator1 = (By.XPATH, f'//*[contains(@name, "{service}")]')
#         element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(element_locator1))
#         location = element.location
#         new_x, new_y = location['x'] + 10, location['y'] + 5
#         TouchAction(driver).tap(x=new_x, y=new_y).perform()
#         driver.implicitly_wait(30)
#         driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="icOutline24Close"]').click()
#
#         # Click CheckBox
#         driver.find_element(By.XPATH,
#                             '//XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeButton[1]').click()
#     except:
#         testWork ='Service'
#         question = f'너는 이제부터 QA 엔지니어야. 너는 지라에 어떠한 이슈를 등록하려고 해. 이슈 내용은 {service}버튼의 동작의 에러 내용이고 이걸 사전조건, 테스트 절차, 실제 결과, 기대결과로 나누어서 작성해야해.'
#         completion = openai.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": question}]
#         )
#         answer = completion.choices[0].message.content
#
#         issue_dict = {
#             'project': {'key': project_key},  # 프로젝트 키
#             'summary': 'Service 화면 테스트 오류',  # 이슈 제목
#             'description': f'{answer}',  # 이슈 설명
#             'issuetype': {'name': issue_type},  # 이슈 타입 (Bug)
#             "assignee": {"accountId": assign_list},  # 담당자 지정
#             "labels": [label_list]  # 여기에 레이블 추가
#         }
#         new_issue = jira.create_issue(fields=issue_dict)
#         issue_link = f"{JIRA_SERVER}/browse/{new_issue.key}"
#         loop.run_until_complete(send_error_message(testWork, issue_link))
#         quit()
#
# def splash_and_intro(worksheet, project_key, issue_type, assign_list, label_list, jira, driver, model):
#     try:
#         splash(driver, model, project_key, issue_type, assign_list, label_list, jira, loop)
#         service(driver, model, project_key, issue_type, assign_list, label_list, jira, loop)
#
#         time.sleep(1)
#         worksheet.update_acell('G9', 'Pass')  # Splash & Intro 화면 확인
#     except Exception as e:
#         worksheet.update_acell('G9', 'Fail')
#         worksheet.update_acell('I9', f"Fail: {e}")
#         quit()
