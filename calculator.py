import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QGridLayout, QPushButton, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MarsCalculator(QWidget):

    def __init__(self):
        super().__init__()
        # 계산에 필요한 현재 수식을 저장하는 변수
        self.current_expression = '' 
        self.initialize_ui()

    def initialize_ui(self):
        # 전체 레이아웃: 결과창이 위에 오고 버튼들이 아래에 오는 수직 구조
        self.main_layout = QVBoxLayout()
        
        # 1. 결과창 설계
        # 아이폰 계산기 특유의 우측 정렬과 여백을 구현하기 위해 LineEdit 속성 조정
        self.display_screen = QLineEdit('0')
        self.display_screen.setReadOnly(True) # 직접 입력 방지
        self.display_screen.setFixedHeight(90)
        self.display_screen.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display_screen.setFont(QFont('Arial', 40))
        
        # 스타일 가이드에 따라 문자열은 ' ' 사용, = 앞뒤 공백 준수
        style_sheet = 'background-color: black; color: white; border: none; padding-right: 20px;'
        self.display_screen.setStyleSheet(style_sheet)
        self.main_layout.addWidget(self.display_screen)

        # 2. 버튼 그리드 레이아웃
        # 5행 4열의 구조를 잡기 위해 QGridLayout 선택
        self.grid_area = QGridLayout()
        self.grid_area.setSpacing(12) # 버튼 간 간격 확보

        # 버튼 생성 및 배치
        # 한 줄씩 손으로 배치하여 UI 레이아웃을 정밀하게 조정함
        
        # 1행: 특수 기능 버튼들
        self.make_button('AC', 0, 0, '#A5A5A5', 'black') # 투명도가 있는 회색 느낌
        self.make_button('+/-', 0, 1, '#A5A5A5', 'black')
        self.make_button('%', 0, 2, '#A5A5A5', 'black')
        self.make_button('/', 0, 3, '#FF9F0A', 'white') # 연산자는 오렌지색

        # 2행: 숫자 7, 8, 9와 곱하기
        self.make_button('7', 1, 0, '#333333', 'white')
        self.make_button('8', 1, 1, '#333333', 'white')
        self.make_button('9', 1, 2, '#333333', 'white')
        self.make_button('*', 1, 3, '#FF9F0A', 'white')

        # 3행: 숫자 4, 5, 6과 빼기
        self.make_button('4', 2, 0, '#333333', 'white')
        self.make_button('5', 2, 1, '#333333', 'white')
        self.make_button('6', 2, 2, '#333333', 'white')
        self.make_button('-', 2, 3, '#FF9F0A', 'white')

        # 4행: 숫자 1, 2, 3과 더하기
        self.make_button('1', 3, 0, '#333333', 'white')
        self.make_button('2', 3, 1, '#333333', 'white')
        self.make_button('3', 3, 2, '#333333', 'white')
        self.make_button('+', 3, 3, '#FF9F0A', 'white')

        # 5행: 0(2칸 차지), 소수점, 결과값
        # 숫자 '0' 버튼은 가로로 길게 배치하기 위해 그리드 인자 조절
        btn_zero = QPushButton('0')
        btn_zero.setFixedSize(152, 70) # 2칸 분량의 가로 길이
        btn_zero.setFont(QFont('Arial', 20))
        btn_zero.setStyleSheet('background-color: #333333; color: white; border-radius: 35px; text-align: left; padding-left: 25px;')
        btn_zero.clicked.connect(self.press_event)
        self.grid_area.addWidget(btn_zero, 4, 0, 1, 2)

        self.make_button('.', 4, 2, '#333333', 'white')
        self.make_button('=', 4, 3, '#FF9F0A', 'white')

        # 최종 레이아웃 합치기
        self.main_layout.addLayout(self.grid_area)
        self.setLayout(self.main_layout)
        
        # 창 속성 설정
        self.setWindowTitle('Mars Calculator 7.0')
        self.setStyleSheet('background-color: black;')
        self.setFixedSize(350, 580)

    def make_button(self, text, row, col, bg_color, fg_color):
        ''' 
        중복 코드를 피하면서도 각각의 버튼을 
        독립적으로 제어하기 위해 커스텀 함수로 구현함
        '''
        button = QPushButton(text)
        button.setFixedSize(70, 70)
        button.setFont(QFont('Arial', 20))
        
        # 아이폰의 둥근 버튼 느낌을 위해 border-radius 적용
        style = f'background-color: {bg_color}; color: {fg_color}; border-radius: 35px;'
        button.setStyleSheet(style)
        
        button.clicked.connect(self.press_event)
        self.grid_area.addWidget(button, row, col)

    def press_event(self):
        '''
        사용자가 버튼을 눌렀을 때의 동작을 정의함>이벤트 핸들러
        '''
        button_target = self.sender()
        button_text = button_target.text()

        if button_text == 'AC':
            # 초기화 로직
            self.current_expression = ''
            self.display_screen.setText('0')
        
        elif button_text == '=':
            # !!!!보너스 과제: 실제 사칙연산 수행!!!!
            try:
                # eval 함수를 사용해 수식을 계산하되, 사용자 편의를 위해 에러 처리 강화
                # x 기호가 들어올 경우를 대비해 변환 로직 포함 가능
                calc_result = str(eval(self.current_expression))
                self.display_screen.setText(calc_result)
                self.current_expression = calc_result # 결과값에서 계속 연산 가능하도록 유지
            except Exception:
                self.display_screen.setText('Error')
                self.current_expression = ''
        
        else:
            # 숫자 및 연산자 입력
            if self.current_expression == '0':
                self.current_expression = button_text
            else:
                self.current_expression += button_text
            self.display_screen.setText(self.current_expression)

if __name__ == '__main__':
    # 프로그램 실행 진입점
    app_inst = QApplication(sys.argv)
    window_view = MarsCalculator()
    window_view.show()
    sys.exit(app_inst.exec())