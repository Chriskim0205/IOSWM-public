from PyQt6.QtWidgets import QApplication, QWidget, QProgressBar, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, \
    QSpacerItem, QSizePolicy, QTextBrowser  # QTextBrowser를 추가
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QMovie
from qt_material import apply_stylesheet
import sys
import os
from openpyxl import load_workbook

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))



class CustomButton(QPushButton):
    def __init__(self, text, icon_name, parent=None):
        super().__init__(text, parent)
        self.setIcon(QIcon.fromTheme(icon_name))
        self.setIconSize(self.size())
        self.setFlat(True)


class ProgressBarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.loading_label.setFixedSize(18, 18)
        self.main_process = None  # main.py 프로세스를 저장하는 변수

    def init_ui(self):

        script_dir = PROJECT_ROOT
        image_dir = os.path.join(script_dir, "assets")
        gif_file_path = os.path.join(image_dir, "loading_resize2.gif")


        self.resize(400, 200)
        self.setWindowTitle("테스트 진행상황")


        main_layout = QVBoxLayout(self)

        # 상단 영역 레이아웃
        top_layout = QVBoxLayout()

        # 수평 레이아웃
        status_layout = QHBoxLayout()

        self.label_status = QLabel("테스트 상태 : ", self)
        self.label_status2 = QLabel("loading...", self)

        # 로딩 이미지
        self.loading_movie = QMovie(gif_file_path)
        self.loading_label = QLabel(self)
        self.loading_label.setMovie(self.loading_movie)
        self.loading_movie.start()

        # 추가된 부분 시작
        spacer = QSpacerItem(0, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        status_layout.addItem(spacer)
        status_layout.addWidget(self.label_status)

        spacer2 = QSpacerItem(-5, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        status_layout.addItem(spacer2)
        status_layout.addWidget(self.label_status2)

        spacer3 = QSpacerItem(0, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        status_layout.addItem(spacer3)
        status_layout.addWidget(self.loading_label)

        spacer4 = QSpacerItem(800, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        status_layout.addItem(spacer4)

        top_layout.addLayout(status_layout)

        main_layout.addLayout(top_layout)

        # 진행률 및 프로그래스 바 레이아웃
        progress_layout = QVBoxLayout()

        self.label_progress = QLabel("진행률 : ", self)
        progress_layout.addWidget(self.label_progress)

        self.prog_bar = QProgressBar(self)
        progress_layout.addWidget(self.prog_bar)

        main_layout.addLayout(progress_layout)

        self.show_hide_button = CustomButton("더 보기 ∨", "arrow-up", self)
        self.show_hide_button.clicked.connect(self.toggle_additional_area)

        # 더보기 버튼 스타일
        self.show_hide_button.setStyleSheet("background-color: #b0e0e6; color: #1e90ff; font-weight: bold;")

        # 수평으로 정렬된 레이아웃 추가
        self.horizontal_layout = QHBoxLayout()

        # 특정한 영역을 감싸는 위젯 추가
        self.additional_area_widget = QWidget(self)
        self.additional_area_widget.setVisible(False)  # 초기에는 숨김
        additional_layout = QVBoxLayout(self.additional_area_widget)


        self.text_browser = QTextBrowser(self.additional_area_widget)
        additional_layout.addWidget(self.text_browser)



        self.horizontal_layout.addWidget(self.additional_area_widget)
        self.horizontal_layout.addWidget(self.show_hide_button, alignment=Qt.AlignmentFlag.AlignRight)  # 버튼 우측 정렬

        main_layout.addLayout(self.horizontal_layout)

        # 진행률 체크 타이머 설정
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress_from_detail)
        self.progress_timer.timeout.connect(self.read_and_update_excel_content)
        self.progress_timer.start(2000)  # 2초마다 업데이트


    def toggle_additional_area(self):

        self.additional_area_widget.setVisible(not self.additional_area_widget.isVisible())

        if self.additional_area_widget.isVisible():
            self.resize(self.width()+ 150, self.height()+ 70 + self.additional_area_widget.height())
        else:
            self.resize(self.width() - 150, self.height()- 70 - self.additional_area_widget.height())


        if self.additional_area_widget.isVisible():
            self.show_hide_button.setText("더보기 ∧")
            self.show_hide_button.setIcon(QIcon.fromTheme("arrow-up"))


            excel_content = self.read_excel_content()
            self.text_browser.setPlainText(excel_content)
        else:
            self.show_hide_button.setText("더보기 ∨")
            self.show_hide_button.setIcon(QIcon.fromTheme("arrow-down"))

    def read_excel_content(self):
        # 엑셀 파일에서 데이터 읽기
        output_strings = None
        try:
            script_dir = PROJECT_ROOT
            image_dir = os.path.join(script_dir, "data")
            excel_file_path = os.path.join(image_dir, "WemixWallet_checklist.xlsx")

            workbook = load_workbook(excel_file_path)
            sheet = workbook['Checklist']  # 체크리스트 탭 선택

            # D열 및 F열 데이터 읽기
            d_values = [str(sheet[f'D{row}'].value) for row in range(6, 64)]
            f_values = [str(sheet[f'F{row}'].value) for row in range(6, 64)]

            # 출력할 문자열 초기화
            output_strings = []

            for d_value, f_value in zip(d_values, f_values):
                if f_value == 'Pass':
                    output_strings.append(f'{d_value} : 완료')

                elif f_value == 'Fail':

                    output_strings.append(f'{d_value} : 실패')

                else:
                    output_strings.append(f'{d_value} : 대기 중...')

            return '\n'.join(output_strings)

        except Exception as e:
            if output_strings is not None:
                return '\n'.join(output_strings)
            else:
                return "데이터를 불러오는 중입니다."

    def reset_progress(self):
        script_dir = PROJECT_ROOT
        progress_dir = os.path.join(script_dir, "data")
        progress_file_path = os.path.join(progress_dir, "progress.txt")

        with open(progress_file_path, "w") as file:
            file.write("0")

    def update_progress_from_detail(self):
        script_dir = PROJECT_ROOT
        progress_dir = os.path.join(script_dir, "data")
        progress_file_path = os.path.join(progress_dir, "progress.txt")

        try:
            with open(progress_file_path, "r") as file:
                progress = int(file.read())
                self.prog_bar.setValue(progress)
                self.update_label_text()
        except FileNotFoundError:
            # 예외 처리: 파일이 없을 경우
            print("Error: progress.txt not found.")
        except ValueError:
            # 예외 처리: 파일 내용이 정수로 변환할 수 없는 경우
            print("Error: Invalid content in progress.txt.")

    def read_and_update_excel_content(self):
        # 엑셀 내용을 읽어와서 텍스트 브라우저에 출력
        excel_content = self.read_excel_content()
        self.text_browser.setPlainText(excel_content)

        try:
            script_dir = PROJECT_ROOT
            image_dir = os.path.join(script_dir, "data")
            excel_file_path = os.path.join(image_dir, "WemixWallet_checklist.xlsx")

            workbook = load_workbook(excel_file_path)
            sheet = workbook['Checklist']  # 체크리스트 탭 선택

            # D열 및 F열 데이터 읽기
            d_values = [str(sheet[f'D{row}'].value) for row in range(6, 64)]
            f_values = [str(sheet[f'F{row}'].value) for row in range(6, 64)]

            # 출력할 문자열 초기화
            output_strings = []

            for d_value, f_value in zip(d_values, f_values):
                if f_value == 'Pass':
                    self.update_scroll()
                elif f_value == 'Fail':
                    self.update_scroll()
                else:
                    output_strings.append(f'{d_value} : 대기 중...')
                    pass
        except Exception as e:
            pass

    def ensure_scroll_visible(self):
        # 커서가 위치한 부분이 화면에 표시되도록 자동으로 스크롤 조정
        self.text_browser.ensureCursorVisible()


    def update_scroll(self):
        # 스크롤을 맨 아래로 이동
        self.text_browser.verticalScrollBar().setValue(self.text_browser.verticalScrollBar().value() + self.text_browser.verticalScrollBar().singleStep())

    def update_label_text(self):
        progress_text = f"진행률 : {self.prog_bar.value()}%"
        self.label_progress.setText(progress_text)

        test_status_text = "준비 중" if self.prog_bar.value() == 0 else \
            "진행 중" if 1 <= self.prog_bar.value() < 100 else \
                "완료"

        self.loading_label.setVisible(self.prog_bar.value() == 0 or (1 <= self.prog_bar.value() < 100))

        # 텍스트 색상 설정
        if self.prog_bar.value() == 0:
            self.label_status2.setStyleSheet("color: #778899")
        elif 1 <= self.prog_bar.value() < 100:
            self.label_status2.setStyleSheet("color: #32cd32")
        else:
            self.label_status2.setStyleSheet("color: #1e90ff")

        self.label_status2.setText(f"{test_status_text}")

    def closeEvent(self, event):
        # 어플리케이션 종료 시 타이머 정지
        self.progress_timer.stop()
        event.accept()

    def resetChecklist(self):
        try:
            script_dir = PROJECT_ROOT
            image_dir = os.path.join(script_dir, "data")
            excel_file_path = os.path.join(image_dir, "WemixWallet_checklist.xlsx")

            # 엑셀 파일 열기
            workbook = load_workbook(excel_file_path)

            # "Checklist" 탭 선택
            sheet = workbook['Checklist']

            # D열 6행부터 60행까지 값을 초기화
            for row in range(6, 64):
                cell = f'F{row}'
                sheet[cell].value = None

            for row in range(6, 64):
                cell = f'H{row}'
                sheet[cell].value = None

            # 변경 내용을 저장
            workbook.save(excel_file_path)

            return True
        except Exception as e:
            print(f"체크리스트 초기화 실패: {e}")
            print(excel_file_path)
            return False

if __name__ == "__main__":
    app = QApplication([])
    window = ProgressBarWindow()
    window.reset_progress()
    window.resetChecklist()
    apply_stylesheet(app, theme='dark_blue.xml')
    window.show()
    sys.exit(app.exec())
