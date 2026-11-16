"""환경 변수 기반 실행 설정.

인증 정보·기기 정보·테스트 지갑 정보는 코드에 두지 않고 `.env` 에서 읽는다.
`.env.example` 을 복사해 값을 채운 뒤 실행한다.
"""
import os

from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


def _required(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"환경 변수 {name} 가 설정되지 않았습니다. .env.example 을 참고하세요.")
    return value


# OpenAI (실패 로그 → 버그 리포트 변환)
OPENAI_API_KEY = _required("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Jira (버그 이슈 자동 등록)
JIRA_SERVER = _required("JIRA_SERVER").rstrip("/")
JIRA_USER = _required("JIRA_USER")
JIRA_API_TOKEN = _required("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = _required("JIRA_PROJECT_KEY")
JIRA_ISSUE_TYPE = os.getenv("JIRA_ISSUE_TYPE", "버그")
JIRA_LABEL = os.getenv("JIRA_LABEL", "WEMIXWALLET")
JIRA_ASSIGNEE_ID = _required("JIRA_ASSIGNEE_ID")
JIRA_BOARD_URL = _required("JIRA_BOARD_URL").rstrip("/")

# Telegram (시작/실패/종료 알림)
TELEGRAM_BOT_TOKEN = _required("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = int(_required("TELEGRAM_CHAT_ID"))

# Google Sheets (체크리스트 결과 기록)
GSPREAD_KEY_FILE = _required("GSPREAD_KEY_FILE")
CHECKLIST_SHEET_URL = _required("CHECKLIST_SHEET_URL")
CHECKLIST_WORKSHEET = os.getenv("CHECKLIST_WORKSHEET", "Checklist")

# Appium / iOS 실기기
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723/wd/hub")
IOS_APP_BUNDLE_ID = os.getenv("IOS_APP_BUNDLE_ID", "com.wemixfoundation.wemixwallet")
IOS_CAPABILITIES = {
    "platformName": "ios",
    "appium:deviceName": _required("IOS_DEVICE_NAME"),
    "appium:platformVersion": _required("IOS_PLATFORM_VERSION"),
    "appium:udid": _required("IOS_UDID"),
    "appium:automationName": "XCUITest",
    "appium:xcodeOrgId": _required("XCODE_ORG_ID"),
    "appium:xcodesigninId": os.getenv("XCODE_SIGNING_ID", "iPhone Developer"),
}

# 테스트 전용 지갑 (실자산이 없는 지갑만 사용)
WALLET_MNEMONIC = _required("WALLET_MNEMONIC")
WALLET_MAIN_PRIVATE_KEY = _required("WALLET_MAIN_PRIVATE_KEY")
WALLET_SECOND_PRIVATE_KEY = _required("WALLET_SECOND_PRIVATE_KEY")
WALLET_ADDRESS = _required("WALLET_ADDRESS")
