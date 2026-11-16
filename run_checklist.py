"""WEMIX Wallet iOS 회귀 체크리스트 실행 진입점.

실기기(XCUITest)에 Appium으로 연결해 scenarios/ 의 시나리오를 체크리스트 순서대로 실행한다.
결과는 Google Sheets 에 기록하고, 실패 시 LLM 리포트 → Jira 이슈 → Telegram 알림 순으로 처리한다.
"""
import asyncio
import time

import gspread
import openai
from appium import webdriver
from appium.options.common import AppiumOptions
from jira import JIRA

from config import (
    APPIUM_SERVER_URL,
    CHECKLIST_SHEET_URL,
    CHECKLIST_WORKSHEET,
    GSPREAD_KEY_FILE,
    IOS_APP_BUNDLE_ID,
    IOS_CAPABILITIES,
    JIRA_API_TOKEN,
    JIRA_ASSIGNEE_ID,
    JIRA_ISSUE_TYPE,
    JIRA_LABEL,
    JIRA_PROJECT_KEY,
    JIRA_SERVER,
    JIRA_USER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)
from reporting.telegram_chat import send_end_message, send_start_message

##################################################################
from scenarios.activate_app import activate_app
from scenarios.add_wallet import add_wallet
from scenarios.ask import ask
from scenarios.auto_lock import auto_lock
from scenarios.bottom_sheet import bottomsheet
from scenarios.change_password import change_password
from scenarios.check_all_explorer import check_all_explorer
from scenarios.check_private_key import private_key
from scenarios.copy_address import copy_address
from scenarios.disconnect_wallet import disconnect_wallet
from scenarios.featured import featured
from scenarios.history import history
from scenarios.history_detail import history_detail
from scenarios.history_explorer import history_explorer
from scenarios.make_new_wallet import make_new_wallet
from scenarios.manage_wallet import manage_wallet
from scenarios.mnemonic import nemonic
from scenarios.my_asset import my_asset
from scenarios.my_asset_receive import my_asset_recieve
from scenarios.my_asset_send import my_asset_send
from scenarios.my_asset_swap import my_asset_swap
from scenarios.news_about_history import news_about_history
from scenarios.nft import nft
from scenarios.notification import norification
from scenarios.poet import poet
from scenarios.policy import policy
from scenarios.qr_check import qr_check
from scenarios.receive import recieve
from scenarios.recover_wallet import recover_wallet
from scenarios.security import security
from scenarios.send import send
from scenarios.session_manage import session_manage
from scenarios.setting_add_wallet import setting_add_wallet
from scenarios.setting_check import setting_check
from scenarios.setting_load_wallet import setting_load_walet
from scenarios.setting_poet import setting_poet
from scenarios.splash_and_intro import splash_and_intro
from scenarios.swap import swap
from scenarios.swap_reverse import swap_reverse
from scenarios.switch_wallet import switch_wallet
from scenarios.total_balance import totalbalance
from scenarios.version import version
from scenarios.wallet_add import wallet_add
from scenarios.wallet_bottom_sheet import wallet_bottomsheet
from scenarios.wallet_change_name import wallet_change_name
from scenarios.wallet_detail_copy import wallet_detail_copy
from scenarios.wallet_load import wallet_load
from scenarios.wrong_send_token import wrong_send_token

# Google Sheets (체크리스트 결과 기록)
gc = gspread.service_account(filename=GSPREAD_KEY_FILE)
doc = gc.open_by_url(CHECKLIST_SHEET_URL)
worksheet = doc.worksheet(CHECKLIST_WORKSHEET)

# Telegram Bot
asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()

# JIRA
jira = JIRA(options={'server': JIRA_SERVER}, basic_auth=(JIRA_USER, JIRA_API_TOKEN))
model = OPENAI_MODEL
project_key = JIRA_PROJECT_KEY
issue_type = JIRA_ISSUE_TYPE
label_list = JIRA_LABEL
assign_list = JIRA_ASSIGNEE_ID

# OpenAI
openai.api_key = OPENAI_API_KEY

##################################################################
start_time = time.time()
loop.run_until_complete(send_start_message())

# # update_app()
# remove_install()


desired_caps_wallet = {**IOS_CAPABILITIES, "appium:app": IOS_APP_BUNDLE_ID}
# Launch the app
driver = webdriver.Remote(APPIUM_SERVER_URL,
                          options=AppiumOptions().load_capabilities(desired_caps_wallet))

activate_app(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
splash_and_intro(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
make_new_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
disconnect_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
recover_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
qr_check(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
norification(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
setting_check(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
wallet_bottomsheet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
add_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
switch_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
manage_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
wallet_add(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
wallet_load(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
bottomsheet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
copy_address(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
totalbalance(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
send(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
recieve(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
worksheet.update_acell('G26', 'Not Test')  # 구매하기 선택 후 이동 확인
my_asset(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
my_asset_send(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
my_asset_recieve(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
my_asset_swap(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
news_about_history(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
poet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
history(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
check_all_explorer(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
history_detail(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
history_explorer(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
swap(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
swap_reverse(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
nft(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
worksheet.update_acell("G42", 'Not Test')  # NILE 둘러보기 선택 후 이동 확인
featured(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
worksheet.update_acell("G44", 'Not Test')  # 보안 설정 > 생체 인식 사용 On 설정 후 동작 확인
worksheet.update_acell("G45", 'Not Test')  # 보안 설정 > 생체 인식 사용 Off 설정 후 동작 확인
change_password(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
auto_lock(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
nemonic(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
setting_add_wallet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
setting_load_walet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
wallet_detail_copy(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
wallet_change_name(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
private_key(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
session_manage(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
setting_poet(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
wrong_send_token(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
ask(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
policy(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
security(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)
version(worksheet, project_key, issue_type, assign_list, label_list, jira, loop, driver, model)

elapsed = time.time() - start_time
loop.run_until_complete(send_end_message(int(elapsed // 60), int(elapsed % 60)))
