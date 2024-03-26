import sys
import re
import platform
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox

#!/usr/bin/env python3
"""
Read_Art.py
rajouter desktop pour lancer en mode interface graphique.

General description:
Ce script contient une application qui permet à l'utilisateur de consulter les articles de la Déclaration des droits de l'Homme. Il propose deux modes d'exécution : console et interface graphique (desktop).

En mode console, l'utilisateur peut saisir un numéro d'article pour afficher le texte correspondant dans la console.
En mode interface graphique, l'utilisateur peut choisir un article à partir d'un menu déroulant pour afficher le texte de l'article dans une fenêtre graphique.

Le script utilise PySide6 pour l'interface graphique et lit les articles à partir d'un fichier texte nommé "declaration1789.txt".
"""

current_os = platform.system()

if current_os != "Windows":
    app = QApplication(sys.argv)
    error_message = "Cette application ne fonctionne que sous Windows."
    QMessageBox.critical(None, "Erreur", error_message)
    sys.exit()


def lire_article(num_article):
    fichier = "declaration1789.txt"
    with open(fichier, 'r', encoding='utf-8') as file:
        current_article_num = None
        current_article_text = ''
        for line in file:
            line = line.strip()
            if line.startswith("Art. "):
                if current_article_num == num_article:
                    return current_article_text
                match = re.match(r'Art\. (\d+)', line)
                if match:
                    current_article_num = int(match.group(1))
                current_article_text = line
            else:
                current_article_text += line + '\n'

        if current_article_num == num_article:
            return current_article_text
        else:
            return "Article non trouvé."

# Code pour la partie console
def Console():
    while True:
        num_article_input = input("Veuillez saisir un nombre entre 1 et 17 (ou 'exit' pour quitter) : ")
        if num_article_input.lower() == "exit":
            break
        if num_article_input.strip() == "":
            print("Veuillez saisir un nombre.")
            continue
        num_article = int(num_article_input)
        if 1 <= num_article <= 17:
            article_text = lire_article(num_article)
            print(f"Article {num_article}:\n{article_text}\n")
        else:
            print("Le nombre doit être entre 1 et 17.")

# Code pour la partie desktop
class ArticleWindow(QMainWindow):
    def __init__(self, article_text):
        super().__init__()
        self.setWindowTitle("Article")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        article_label = QLabel(article_text)
        layout.addWidget(article_label)
        self.central_widget.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Déclaration des droits de l'Homme")
        self.setGeometry(100, 100, 400, 300)

        self.setWindowIcon(QIcon("cartman.jpg"))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        welcome_label = QLabel("Bienvenue ! Veuillez choisir un article :")
        layout.addWidget(welcome_label)

        self.article_combobox = QComboBox()
        for i in range(1, 18):
            self.article_combobox.addItem(str(i))

        self.article_combobox.currentIndexChanged.connect(self.show_article_window)

        layout.addWidget(self.article_combobox)

        self.central_widget.setLayout(layout)

        self.article_window = None

    def show_article_window(self):
        article_index = self.article_combobox.currentIndex() + 1
        article_text = lire_article(article_index)
        if self.article_window:
            self.article_window.close()
        self.article_window = ArticleWindow(article_text)
        self.article_window.show()

# Lancement de l'application en fonction du mode d'exécution
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "desktop":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        Console()