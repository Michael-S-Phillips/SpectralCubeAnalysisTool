import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot
import logging

class RelabIntegrationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText("Enter search term...")
        self.layout.addWidget(self.searchLineEdit)

        self.searchButton = QPushButton("Search")
        self.layout.addWidget(self.searchButton)
        self.searchButton.clicked.connect(self.searchRelabDatabase)

        self.resultsListWidget = QListWidget()
        self.layout.addWidget(self.resultsListWidget)

        self.setLayout(self.layout)
        logging.info("RELAB Integration Widget initialized.")

    @pyqtSlot()
    def searchRelabDatabase(self):
        searchTerm = self.searchLineEdit.text()
        if not searchTerm.strip():
            QMessageBox.warning(self, "Search Error", "Please enter a valid search term.")
            return

        # Actual URL for the RELAB database search API endpoint needs to be provided here
        searchUrl = "https://pds-speclib.rsl.wustl.edu/search.aspx"  # INPUT_REQUIRED {Replace with the actual RELAB database search API endpoint}
        params = {'q': searchTerm}

        try:
            response = requests.get(searchUrl, params=params)
            if response.status_code == 200:
                try:
                    results = response.json()
                    self.resultsListWidget.clear()
                    for result in results:
                        if 'name' in result:
                            self.resultsListWidget.addItem(result['name'])
                        else:
                            logging.warning("Skipping result due to missing 'name' field")
                    logging.info("Search completed successfully.")
                except ValueError:
                    logging.error("Failed to parse JSON response", exc_info=True)
                    QMessageBox.warning(self, "Search Error", "Invalid response format.")
            else:
                logging.error(f"Failed to search RELAB database. Status code: {response.status_code}")
                QMessageBox.warning(self, "Search Error", f"Failed to search RELAB database. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error("Failed to search RELAB database", exc_info=True)
            QMessageBox.critical(self, "Search Error", f"Failed to search RELAB database: {e}")