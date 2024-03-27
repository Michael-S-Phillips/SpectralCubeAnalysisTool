from PyQt5.QtWidgets import QMainWindow, QListWidget, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from image_window import ImageWindow
import logging

class ImageManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Management")
        self.setGeometry(100, 100, 400, 300)  # Position x, y, width, height

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout()

        self.imageListWidget = QListWidget()
        layout.addWidget(self.imageListWidget)

        self.openImageButton = QPushButton("Open Image")
        self.openImageButton.clicked.connect(self.openImage)
        layout.addWidget(self.openImageButton)

        self.centralWidget.setLayout(layout)
        self.imageWindows = []

        logging.info("Image Management Window initialized.")

    @pyqtSlot()
    def openImage(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.tif *.tiff *.img)")
        if filename:
            try:
                imageWindow = ImageWindow(filename)
                imageWindow.show()
                self.imageWindows.append(imageWindow)
                self.imageListWidget.addItem(filename)
                logging.info(f"Opened image: {filename}")
            except Exception as e:
                logging.error("Error opening image: %s", e, exc_info=True)
                QMessageBox.critical(self, "Error", "An error occurred while opening the image.")