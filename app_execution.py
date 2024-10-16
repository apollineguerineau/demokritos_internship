# main.py
import sys
from PyQt5.QtWidgets import QApplication
from app.view.view import MainWindow
from app.view.export_session_view import ExportSessionWindow
from app.presenters.presenter import CrawlerPresenter

def main():
    app = QApplication(sys.argv)

    presenter = CrawlerPresenter(None, None)  # À remplacer par votre logique de création de la vue
    view = MainWindow(presenter)
    view_export = ExportSessionWindow(presenter)
    presenter.view = view
    presenter.view_export = view_export

    # Afficher la fenêtre principale
    view.show()

    # Exécuter l'application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
