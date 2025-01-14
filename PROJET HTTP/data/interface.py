import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QWidget
)
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt
import asyncio
from http_client import download_http11, download_http2, download_http3, download_http10
from performance import measure_http_performance, measure_http_performance_async


class HTTPTesterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTTP TEST")
        self.setGeometry(100, 100, 600, 400)

        # Variables pour stocker les performances
        self.results = {}

        # Widget principal
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout()

        # Champ URL
        self.url_label = QLabel("Entrez l'URL :", self)
        self.url_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.url_label)

        self.url_input = QLineEdit(self)
        self.layout.addWidget(self.url_input)

        # Boutons pour tester les performances HTTP
        self.http10_button = QPushButton("Tester HTTP/1.0", self)
        self.http10_button.clicked.connect(self.test_http10)
        self.layout.addWidget(self.http10_button)

        self.http11_button = QPushButton("Tester HTTP/1.1", self)
        self.http11_button.clicked.connect(self.test_http11)
        self.layout.addWidget(self.http11_button)

        self.http2_button = QPushButton("Tester HTTP/2", self)
        self.http2_button.clicked.connect(self.test_http2)
        self.layout.addWidget(self.http2_button)

        self.http3_button = QPushButton("Tester HTTP/3", self)
        self.http3_button.clicked.connect(self.test_http3)
        self.layout.addWidget(self.http3_button)

        # Bouton pour afficher le graphique
        self.plot_button = QPushButton("Afficher le graphique des performances", self)
        self.plot_button.clicked.connect(self.plot_results)
        self.layout.addWidget(self.plot_button)

        # Bouton pour télécharger la page
        self.download_page_button = QPushButton("Télécharger la page", self)
        self.download_page_button.clicked.connect(self.download_page)
        self.layout.addWidget(self.download_page_button)

        # Zone de résultats
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def test_http10(self):
        """Test HTTP/1.0 et affiche les résultats."""
        url = self.url_input.text()
        if url:
            try:
                self.result_area.append(f"Test HTTP/1.0 pour l'URL : {url}")
                time_taken = measure_http_performance(url, download_http10)
                self.results["HTTP/1.0"] = time_taken
                self.result_area.append(f"Temps HTTP/1.0 : {time_taken:.2f} secondes\n")
            except Exception as e:
                self.result_area.append(f"Erreur HTTP/1.0 : {str(e)}")
        else:
            self.result_area.append("Veuillez entrer une URL valide.")

    def test_http11(self):
        """Test HTTP/1.1 et affiche les résultats."""
        url = self.url_input.text()
        if url:
            try:
                self.result_area.append(f"Test HTTP/1.1 pour l'URL : {url}")
                time_taken = measure_http_performance(url, download_http11)
                self.results["HTTP/1.1"] = time_taken
                self.result_area.append(f"Temps HTTP/1.1 : {time_taken:.2f} secondes\n")
            except Exception as e:
                self.result_area.append(f"Erreur HTTP/1.1 : {str(e)}")
        else:
            self.result_area.append("Veuillez entrer une URL valide.")

    def test_http2(self):
        """Test HTTP/2 et affiche les résultats."""
        url = self.url_input.text()
        if url:
            try:
                self.result_area.append(f"Test HTTP/2 pour l'URL : {url}")
                time_taken = asyncio.run(measure_http_performance_async(url, download_http2))
                self.results["HTTP/2"] = time_taken
                self.result_area.append(f"Temps HTTP/2 : {time_taken:.2f} secondes\n")
            except Exception as e:
                self.result_area.append(f"Erreur HTTP/2 : {str(e)}")
        else:
            self.result_area.append("Veuillez entrer une URL valide.")

    def test_http3(self):
        """Test HTTP/3 et affiche les résultats."""
        url = self.url_input.text()
        if url:
            try:
                self.result_area.append(f"Test HTTP/3 pour l'URL : {url}")
                time_taken = asyncio.run(measure_http_performance_async(url, download_http3))
                self.results["HTTP/3"] = time_taken
                self.result_area.append(f"Temps HTTP/3 : {time_taken:.2f} secondes\n")
            except Exception as e:
                self.result_area.append(f"Erreur HTTP/3 : {str(e)}")
        else:
            self.result_area.append("Veuillez entrer une URL valide.")

    def plot_results(self):
        """Affiche un graphe des performances HTTP et l'enregistre dans le dossier 'plots'."""
        if not self.results:
            self.result_area.append("Aucun résultat à afficher. Veuillez effectuer les tests d'abord.")
            return

        protocols = list(self.results.keys())
        times = list(self.results.values())

        # Créer le graphique
        plt.bar(protocols, times, color=['blue', 'green', 'black', 'red'])
        plt.xlabel("Protocole HTTP")
        plt.ylabel("Temps (secondes)")
        plt.title("Comparaison des performances HTTP")

        # Sauvegarder le graphique
        os.makedirs("plots", exist_ok=True)  # Crée le dossier plots s'il n'existe pas
        file_path = os.path.join("plots", "http_performance.png")
        plt.savefig(file_path)
        self.result_area.append(f"Graphique enregistré dans : {file_path}")

        # Afficher le graphique
        plt.show()

    def download_page(self):
        """Télécharge le contenu de la page et le sauvegarde dans le dossier 'pages'."""
        url = self.url_input.text()
        if url:
            try:
                self.result_area.append(f"Téléchargement de la page : {url}")
                # Utilisation de download_http11 pour télécharger le contenu
                content = download_http11(url)
                os.makedirs("pages", exist_ok=True)  # Crée le dossier pages s'il n'existe pas
                file_name = os.path.join("pages", "downloaded_page.html")
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(content)
                self.result_area.append(f"Page enregistrée dans : {file_name}\n")
            except Exception as e:
                self.result_area.append(f"Erreur lors du téléchargement : {str(e)}")
        else:
            self.result_area.append("Veuillez entrer une URL valide.")


if __name__ == "__main__":
    app = QApplication([])
    window = HTTPTesterApp()
    window.show()
    app.exec()
