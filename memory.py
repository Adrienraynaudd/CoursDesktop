import sys
from random import shuffle
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PySide6.QtCore import QTimer

class MemoryGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.flipped_cards = []

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
        if button in self.flipped_cards:
            return
        
        index = self.buttons.index(button)
        card = self.cards[index]
        button.setText(card)
        button.setStyleSheet('color: black')
        button.setEnabled(False)
        self.flipped_cards.append(button)
        
        if len(self.flipped_cards) == 2:
            QTimer.singleShot(1000, self.checkCards)

    def checkCards(self):
        if self.flipped_cards[0].text() != self.flipped_cards[1].text():
            for btn in self.flipped_cards:
                btn.setText(' ')
                btn.setEnabled(True)
        self.flipped_cards.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MemoryGame()
    sys.exit(app.exec())
