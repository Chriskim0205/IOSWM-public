import os
import sys

import openai
from PyPDF2 import PdfReader

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import OPENAI_API_KEY  # noqa: E402

openai.api_key = OPENAI_API_KEY
pdfreader = PdfReader(sys.argv[1])  # 기획서/화면 정의서 PDF 경로
pages = pdfreader.pages
text = ''
for page in pages:
    sub = page.extract_text()
    text += sub
    print('\n')
print(text)

# question = (f'{text} 기반으로 작성해야하는 테스트 케이스를 TC summary, Pre Condition, Procedure, Expected Result 형식으로 나누어서 테스트 케이스를 한글로 작성해줘.'
#             f'동작 검증의 경우 '
#             f'TC summary는 무슨 화면에서 무슨 동작 검증을 하고있는지 작성해.'
#             f'Pre Condition은 웹페이지 진입으로 작성해.'
#             f'Procedure는 무조건 로그인 화면에서 시작해서 해당 화면으로 이동해서 버튼 선택 이전까지 모든 절차를 나열하도록 작성해.'
#             f'Expected Result는 해당 검증 시 기대 결과를 작성해.'
#             f'문구 검증의 경우'
#             f'TC summary는 무슨 화면에서 무슨 문구 검증을 하고있는지 작성해.'
#             f'Pre Condition은 웹페이지 진입으로 작성해.'
#             f'Procedure는 무조건 인트로 화면에서 시작해서 해당 화면으로 이동해서 문구 출력 이전까지 모든 절차를 나열하도록 작성해.'
#             f'Expected Result는 "A" 문구 확인 형식으로 작성해.'
#             f'각 행마다 무조건 하나의 테스트 케이스로 작성해. 모든 동작 및 문구에 대한 태스트 케이스를 작성해야해. 그리고 각 케이스마다 TC 번호를 기입해줘.'
#             )
#
# completion = openai.chat.completions.create(
#     model='gpt-3.5-turbo',
#     messages=[{"role": "assistant", "content": question}]
# )
# answer = completion.choices[0].message.content
# print(answer)
#
