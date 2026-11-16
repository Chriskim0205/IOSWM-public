from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout, QWidget, QHBoxLayout, \
    QPushButton, QMessageBox, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation
from qt_material import apply_stylesheet
import os
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Toast(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #333; color: white; border-radius: 5px;")
        self.setFixedHeight(50)
        self.setFixedWidth(300)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(3000)  # 토스트의 표시 시간 (1000 밀리초 = 1초)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)

    def show_toast(self):
        self.animation.start()
        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.setWindowTitle("자동화 테스트 도우미")
        self.resize(350, 350)
        layout_project = QHBoxLayout()
        label1 = QLabel("프로젝트 이름", self)
        label1.setStyleSheet("font-size: 14pt;")
        layout_project.addWidget(label1)
        self.combo_project = QComboBox(self)
        self.combo_project.addItems(["WEMIX Wallet", "Wepublic Wallet", "The Pol"])
        self.combo_project.setStyleSheet("font-size: 14pt; color : #dcdcdc;")
        layout_project.addWidget(self.combo_project)
        layout.addLayout(layout_project)

        layout_os = QHBoxLayout()
        label2 = QLabel("기기 OS", self)
        label2.setStyleSheet("font-size: 14pt;")
        layout_os.addWidget(label2)
        self.combo_os = QComboBox(self)
        self.combo_os.addItems(["안드로이드", "iOS"])
        self.combo_os.setStyleSheet("font-size: 14pt; color : #dcdcdc;")
        layout_os.addWidget(self.combo_os)
        layout.addLayout(layout_os)

        layout_test_type = QHBoxLayout()
        label3 = QLabel("테스트 종류", self)
        label3.setStyleSheet("font-size: 14pt;")
        layout_test_type.addWidget(label3)
        self.combo_test_type = QComboBox(self)
        self.combo_test_type.addItems(["기본 체크리스트", "Full Test", "탐색적 테스트"])
        self.combo_test_type.setStyleSheet("font-size: 14pt; color : #dcdcdc; ")
        layout_test_type.addWidget(self.combo_test_type)
        layout.addLayout(layout_test_type)

        info_label = QLabel("* 테스트 정보를 선택한 후에 실행 버튼을 눌러주세요.", self)
        info_label.setStyleSheet("font-size: 12pt; color: gray;")
        layout.addWidget(info_label)

        button_layout = QHBoxLayout()
        cancel_button = QPushButton("닫기", self)
        cancel_button.setStyleSheet("font-size: 14pt;")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        run_button = QPushButton("실행", self)
        run_button.setStyleSheet("font-size: 14pt;")
        run_button.clicked.connect(self.execute_action)
        button_layout.addWidget(run_button)
        layout.addLayout(button_layout)

    # 프로그래스 파일을 시작할 때 0으로 만듬
    def reset_progress(self):
        progress_file_path = os.path.join(PROJECT_ROOT, "data", "progress.txt")
        with open(progress_file_path, "w") as file:
            file.write("0")

    def execute_action(self):
        selected_project = self.combo_project.currentText()
        selected_os = self.combo_os.currentText()
        selected_test_type = self.combo_test_type.currentText()

        if selected_project == "WEMIX Wallet" and selected_os == "iOS" and selected_test_type == "기본 체크리스트":
            main_py_path = os.path.join(PROJECT_ROOT, "run_checklist.py")
            detail_py_path = os.path.join(PROJECT_ROOT, "gui", "progress_view.py")

            # 실행 중인 main.py와 detail.py의 프로세스를 생성
            main_process = subprocess.Popen([sys.executable, main_py_path], cwd=PROJECT_ROOT)
            detail_process = subprocess.Popen([sys.executable, detail_py_path], cwd=PROJECT_ROOT)

            toast = Toast("테스트를 시작합니다. \n * 테스트 예상 시간 : 7 ~ 10 분", self)
            toast.show_toast()
        else:
            QMessageBox.warning(self, "알림", "해당 테스트는 준비중입니다.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    apply_stylesheet(app, theme='dark_blue.xml')

    window.show()
    sys.exit(app.exec())
