import sys
from random import shuffle
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

class MemoryGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Memory Game')
        self.resize(800, 600)
        self.grid = QGridLayout()
        self.cards = [str(i) for i in range(1, 9)] * 2
        shuffle(self.cards)
        self.buttons = []
        for row in range(4):
            for col in range(4):
                btn = QPushButton(' ', self)
                btn.clicked.connect(self.cardClicked)
                btn.setFixedSize(100, 100)
                self.buttons.append(btn)
                self.grid.addWidget(btn, row, col)
        self.setLayout(self.grid)
        self.show()

    def cardClicked(self):
        button = self.sender()
        index = self.buttons.index(button)
        card = self.cards[index]
        button.setText(card)
        button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MemoryGame()
    sys.exit(app.exec())
