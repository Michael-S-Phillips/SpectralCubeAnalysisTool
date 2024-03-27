from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
import logging

class BandSelectionWidget(QWidget):
    bandsSelected = pyqtSignal(list)

    def __init__(self, dataset):
        super().__init__()
        self.dataset = dataset
        self.layout = QVBoxLayout()

        self.redBandComboBox = QComboBox()
        self.greenBandComboBox = QComboBox()
        self.blueBandComboBox = QComboBox()

        self.populateBandSelectionDropdowns()

        self.applyBandsButton = QPushButton("Apply RGB Bands")
        self.applyBandsButton.clicked.connect(self.emitSelectedBands)

        self.layout.addWidget(self.redBandComboBox)
        self.layout.addWidget(self.greenBandComboBox)
        self.layout.addWidget(self.blueBandComboBox)
        self.layout.addWidget(self.applyBandsButton)

        self.setLayout(self.layout)
        logging.info("BandSelectionWidget initialized.")

    def populateBandSelectionDropdowns(self):
        try:
            for i in range(1, self.dataset.RasterCount + 1):
                bandStr = str(i)
                self.redBandComboBox.addItem(bandStr)
                self.greenBandComboBox.addItem(bandStr)
                self.blueBandComboBox.addItem(bandStr)
            logging.info("Band selection dropdowns populated.")
        except Exception as e:
            logging.error("Error populating band selection dropdowns: %s", str(e), exc_info=True)
            QMessageBox.critical(self, "Error", "An error occurred while populating band selection dropdowns.")

    def emitSelectedBands(self):
        try:
            redBand = int(self.redBandComboBox.currentText())
            greenBand = int(self.greenBandComboBox.currentText())
            blueBand = int(self.blueBandComboBox.currentText())
            if redBand == greenBand or greenBand == blueBand or redBand == blueBand:
                raise ValueError("Please select different bands for R, G, and B.")
            self.bandsSelected.emit([redBand, greenBand, blueBand])
            logging.info("RGB bands selected successfully.")
        except ValueError as e:
            logging.error("Error selecting RGB bands: %s", str(e), exc_info=True)
            QMessageBox.warning(self, "Invalid Band Selection", str(e))
        except Exception as e:
            logging.error("Error selecting RGB bands: %s", str(e), exc_info=True)
            QMessageBox.critical(self, "Error", "An error occurred while selecting RGB bands.")