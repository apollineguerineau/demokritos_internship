# view/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt

from app.view.export_session_view import ExportSessionWindow

class MainWindow(QMainWindow):
    def __init__(self, presenter):
        super().__init__()

        self.presenter = presenter
        self.setWindowTitle("Crawler Configuration")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

       # Add a button to open the export session window
        self.export_button = QPushButton("Exporter une session", self)
        self.export_button.clicked.connect(self.open_export_window)
        layout.addWidget(self.export_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Input for session name
        self.session_name_input = QLineEdit(self)
        self.session_name_input.setPlaceholderText("Nom de la session")
        layout.addWidget(QLabel("Nom de la session"))
        layout.addWidget(self.session_name_input)

        # Input for query
        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Requête")
        layout.addWidget(QLabel("Requête de recherche"))
        layout.addWidget(self.query_input)

        # Button to choose a file
        self.seed_file_path_input = QLineEdit(self)
        self.seed_file_path_input.setPlaceholderText("Choose a file for seed pages")
        layout.addWidget(QLabel("File"))
        layout.addWidget(self.seed_file_path_input)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        # Dropdown for searcher
        self.searcher_choice = QComboBox(self)
        self.searcher_choice.addItems(["ZenodoSearcher"])
        layout.addWidget(QLabel("Choisir un searcher"))
        layout.addWidget(self.searcher_choice)

        # Input for nb new pages per request
        self.nb_page_per_request_input = QLineEdit(self)
        self.nb_page_per_request_input.setPlaceholderText("nb page per request")
        layout.addWidget(self.nb_page_per_request_input)

        # Dropdown for sorter choice
        self.classifier_model_choice = QComboBox(self)
        self.classifier_model_choice.addItems(["RandomSorter", "ClassifierSorter"])
        layout.addWidget(QLabel("Sorter choice"))
        layout.addWidget(self.classifier_model_choice)

        # New dropdown for type classifier choice (initially hidden)
        self.classifier_choice = QComboBox(self)
        self.classifier_choice.addItems(["TransformerBasedClassifier"])
        layout.addWidget(self.classifier_choice)
        self.classifier_choice.setVisible(False)

        # Input for model and tokenizer path (initially hidden)
        self.model_path_input = QLineEdit(self)
        self.model_path_input.setPlaceholderText("path to model")
        layout.addWidget(self.model_path_input)
        self.model_path_input.setVisible(False)

        self.tokenizer_path_input = QLineEdit(self)
        self.tokenizer_path_input.setPlaceholderText("path to tokenizer")
        layout.addWidget(self.tokenizer_path_input)
        self.tokenizer_path_input.setVisible(False)

        # Dropdown for query expander
        self.query_expander_choice = QComboBox(self)
        self.query_expander_choice.addItems(["NoQueryExpander", "LLMQueryExpander"])
        layout.addWidget(QLabel("Choisir un query expander"))
        layout.addWidget(self.query_expander_choice)

        # New dropdown for template choice (initially hidden)
        self.template_choice = QComboBox(self)
        self.template_choice.addItems(["SeedQueryBasedTemplate", "CurrentQueryBasedTemplate"])
        layout.addWidget(self.template_choice)
        self.template_choice.setVisible(False)

        # Input for script (initially hidden)
        self.script_input = QLineEdit(self)
        self.script_input.setPlaceholderText("Your task is to expand this request : {}. Please generate one additional term that might help retrieve more relevant results in a broader context. The goal is to give a synonym, a related term, or any other variation that could improve the search results. Your response must be only one term and the output must be in json format with key 'related_term'.")
        layout.addWidget(self.script_input)
        self.script_input.setVisible(False)

        # Input for LLM model (initially hidden)
        self.llm_input = QLineEdit(self)
        self.llm_input.setPlaceholderText("LLM model to use")
        layout.addWidget(self.llm_input)
        self.llm_input.setVisible(False)

        # New dropdown for LLM framework choice (initially hidden)
        self.framework_choice = QComboBox(self)
        self.framework_choice.addItems(["Ollama", "HuggingFace", "OpenAI"])
        layout.addWidget(self.framework_choice)
        self.framework_choice.setVisible(False)

        # Dropdown for stop criteria
        self.stop_criteria_choice = QComboBox(self)
        self.stop_criteria_choice.addItems(["NbRelevantStopCriteria", "TimeCriteria"])
        layout.addWidget(QLabel("Stop criteria choice"))
        layout.addWidget(self.stop_criteria_choice)

        # Input for number of relevant pages (initially hidden)
        self.relevant_pages_input = QLineEdit(self)
        self.relevant_pages_input.setPlaceholderText("Nombre de pages")
        layout.addWidget(self.relevant_pages_input)
        self.relevant_pages_input.setVisible(True)

        # Button to run the crawler
        self.run_button = QPushButton("Lancer le crawl", self)
        self.run_button.clicked.connect(self.run_crawl)
        layout.addWidget(self.run_button)

        # Set layout in QWidget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect the query expander selection to show/hide template and script
        self.searcher_choice.currentIndexChanged.connect(self.toggle_for_searcher)
        self.classifier_model_choice.currentIndexChanged.connect(self.toggle_for_classifier)
        self.query_expander_choice.currentIndexChanged.connect(self.toggle_for_llm_exansor)
        self.stop_criteria_choice.currentIndexChanged.connect(self.toggle_relevant_pages_input)

    def open_export_window(self):
            self.export_window = ExportSessionWindow(self.presenter)
            self.export_window.show()

    def toggle_for_searcher(self) : 
        if self.searcher_choice.currentText() == "ZenodoSearcher":
            self.nb_page_per_request_input.setVisible(True)
        else:
            self.nb_page_per_request_input.setVisible(False)
    
    def toggle_for_classifier(self):
        # Show or hide the template and script input based on the selected query expander
        if self.classifier_model_choice.currentText() == "ClassifierSorter":
            self.classifier_choice.setVisible(True)
            self.model_path_input.setVisible(True)
            self.tokenizer_path_input.setVisible(True)
        else:
            self.classifier_choice.setVisible(False)
            self.model_path_input.setVisible(False)
            self.tokenizer_path_input.setVisible(False)

    def toggle_for_llm_exansor(self):
        # Show or hide the template and script input based on the selected query expander
        if self.query_expander_choice.currentText() == "LLMQueryExpander":
            self.template_choice.setVisible(True)
            self.script_input.setVisible(True)
            self.llm_input.setVisible(True)
            self.framework_choice.setVisible(True)
        else:
            self.template_choice.setVisible(False)
            self.script_input.setVisible(False)
            self.llm_input.setVisible(False)
            self.framework_choice.setVisible(False)

    def toggle_relevant_pages_input(self):
        # Show or hide the relevant pages input based on the selected stop criteria
        if self.stop_criteria_choice.currentText() == "NbRelevantStopCriteria":
            self.relevant_pages_input.setVisible(True)
        else:
            self.relevant_pages_input.setVisible(False)

    # Function to browse files
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisissez un fichier", "", "Tous les fichiers (*)")
        if file_path:
            self.seed_file_path_input.setText(file_path)

    # Functions to get user input
    def get_session_name(self):
        return self.session_name_input.text()

    def get_query(self):
        return self.query_input.text()
    
    def get_seed_page_file(self):
        return self.seed_file_path_input.text()

    def get_searcher_choice(self):
        return self.searcher_choice.currentText()
    
    def get_nb_page_per_request(self):
        return self.nb_page_per_request_input.text()

    def get_sorter_choice(self):
        return self.classifier_model_choice.currentText()
    
    def get_classifier_choice(self):
        return self.classifier_choice.currentText()

    def get_model_path(self):
        return self.model_path_input.text()
    
    def get_tokenizer_path(self):
        return self.tokenizer_path_input.text()

    def get_query_expander_choice(self):
        return self.query_expander_choice.currentText()

    def get_template_choice(self):
        return self.template_choice.currentText()

    def get_script(self):
        return self.script_input.text()
    
    def get_framework(self):
        return self.framework_choice.currentText()
    
    def get_llm_model(self):
        return self.llm_input.text()

    def get_stop_criteria_choice(self):
        return self.stop_criteria_choice.currentText()

    def get_nb_relevant_pages(self):
        # Return the number of relevant pages as an integer
        return int(self.relevant_pages_input.text()) if self.relevant_pages_input.isVisible() else None

    # Function to run the crawl
    def run_crawl(self):
        self.presenter.configure_crawler()

    # Function to show a message to the user
    def show_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.exec_()


