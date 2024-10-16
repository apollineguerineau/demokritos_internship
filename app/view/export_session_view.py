from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QComboBox, QPushButton, QWidget, QFileDialog, QMessageBox
import csv

class ExportSessionWindow(QMainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.setWindowTitle("Exporter une session")
        self.setGeometry(200, 200, 400, 200)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Dropdown to select a session
        self.session_dropdown = QComboBox(self)
        sessions = self.presenter.get_all_sessions()  # Retrieve all sessions (id, name)
        
        # Add sessions to the dropdown
        for session_id, session_name in sessions:
            self.session_dropdown.addItem(session_name, session_id)
        
        layout.addWidget(QLabel("Sélectionnez une session à exporter"))
        layout.addWidget(self.session_dropdown)

        # Button to export the selected session
        self.export_button = QPushButton("Exporter", self)
        self.export_button.clicked.connect(self.export_session_to_csv)
        layout.addWidget(self.export_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def export_session_to_csv(self):
        # Get the selected session ID
        session_id = self.session_dropdown.currentData()

        # Retrieve the session data from the presenter
        session_data = self.presenter.get_session_data_by_id(session_id)
        if not session_data:
            return

        # Open file dialog to choose the destination CSV file
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "Fichiers CSV (*.csv)")
        
        if file_path:
            # Write session data to CSV
            self.write_session_to_csv(file_path, session_data)

    def write_session_to_csv(self, file_path, session_data):
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write headers
                writer.writerow(['url', 'title', 'description', 'publication_date', 'authors', 'language', 'notes'])

                # Write page data
                for page in session_data['pages']:
                    writer.writerow([
                        page.url,
                        page.title,
                        page.description,
                        page.publication_date,
                        page.authors,
                        page.language,
                        page.notes,
                    ])

            QMessageBox.information(self, "Succès", "Les données ont été exportées avec succès !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'exportation : {e}")

    
