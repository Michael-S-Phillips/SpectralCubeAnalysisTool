from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout, QMessageBox
import logging

class BandSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select RGB Bands")
        self.layout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.redBandEdit = QLineEdit()
        self.greenBandEdit = QLineEdit()
        self.blueBandEdit = QLineEdit()

        self.formLayout.addRow(QLabel("Red Band:"), self.redBandEdit)
        self.formLayout.addRow(QLabel("Green Band:"), self.greenBandEdit)
        self.formLayout.addRow(QLabel("Blue Band:"), self.blueBandEdit)

        self.layout.addLayout(self.formLayout)

        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        self.layout.addWidget(self.okButton)
        self.layout.addWidget(self.cancelButton)

        self.setLayout(self.layout)

    def getBands(self):
        try:
            redBand = int(self.redBandEdit.text())
            greenBand = int(self.greenBandEdit.text())
            blueBand = int(self.blueBandEdit.text())
            logging.info("RGB bands selected successfully.")
            return redBand, greenBand, blueBand
        except ValueError as e:
            logging.error("Error in selecting RGB bands: %s", str(e), exc_info=True)
            QMessageBox.critical(self, "Invalid Input", "Please enter valid band numbers.")
            return None, None, None