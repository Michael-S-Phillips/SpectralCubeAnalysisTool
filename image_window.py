from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox, QStatusBar, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from osgeo import gdal
import numpy as np
import logging
import spectral
import os

class ImageWindow(QMainWindow):
    def __init__(self, imagePath):
        super().__init__()
        self.setWindowTitle("Image Window")
        self.setGeometry(100, 100, 600, 400)  # Position x, y, width, height

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setMouseTracking(True)  # Enable mouse tracking on the central widget
        layout = QVBoxLayout()

        self.imageLabel = QLabel("Image loaded. Hover over the image for coordinates.")
        layout.addWidget(self.imageLabel)

        # Dropdowns for selecting RGB bands
        bandSelectionLayout = QHBoxLayout()
        self.redBandComboBox = QComboBox()
        self.greenBandComboBox = QComboBox()
        self.blueBandComboBox = QComboBox()
        self.applyBandsButton = QPushButton("Apply RGB Bands")
        
        bandSelectionLayout.addWidget(QLabel("R"))
        bandSelectionLayout.addWidget(self.redBandComboBox)
        bandSelectionLayout.addWidget(QLabel("G"))
        bandSelectionLayout.addWidget(self.greenBandComboBox)
        bandSelectionLayout.addWidget(QLabel("B"))
        bandSelectionLayout.addWidget(self.blueBandComboBox)
        layout.addLayout(bandSelectionLayout)
        layout.addWidget(self.applyBandsButton)

        self.centralWidget.setLayout(layout)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.setMouseTracking(True)  # Enable mouse tracking on the window

        self.defaultBands = [1, 2, 3]  # Default bands for RGB display
        self.displayMode = 'RGB'  # Default display mode
        self.loadAndDisplayImage(imagePath)

        self.applyBandsButton.clicked.connect(self.applySelectedBands)

    def loadAndDisplayImage(self, imagePath, bands=None, displayMode=None):
        try:
            self.dataset = gdal.Open(imagePath)
            if self.dataset is None:
                raise Exception("Failed to open the image file.")
            
            # Populate RGB band selection dropdowns
            self.populateBandSelectionDropdowns(imagePath)

            if displayMode is not None:
                self.displayMode = displayMode

            if self.displayMode == 'RGB':
                if bands is None:
                    bands = self.defaultBands
                
                if len(bands) != 3:
                    raise ValueError("Exactly three bands must be provided for RGB display.")
                
                # Read bands for RGB
                band_data = []
                for band in bands:
                    if band > self.dataset.RasterCount or band < 1:
                        raise ValueError(f"Band number {band} is out of range for this dataset.")
                    band_data.append(self.dataset.GetRasterBand(band).ReadAsArray())

                # Stack arrays to form an RGB image
                rgb_array = np.dstack(band_data)

                # Normalize each channel to 0-255
                rgb_normalized = np.zeros_like(rgb_array, dtype=np.uint8)
                for i in range(3):
                    channel = rgb_array[:, :, i]
                    if np.any(channel != channel.min()):
                        rgb_normalized[:, :, i] = ((channel - channel.min()) / (channel.max() - channel.min()) * 255).astype(np.uint8)
                    else:
                        rgb_normalized[:, :, i] = np.zeros_like(channel, dtype=np.uint8)

                # Convert the normalized array to QImage
                height, width, _ = rgb_normalized.shape
                bytesPerLine = 3 * width
                image = QImage(rgb_normalized.data.tobytes(), width, height, bytesPerLine, QImage.Format_RGB888)
            elif self.displayMode == 'Grayscale':
                band = self.dataset.GetRasterBand(1)
                array = band.ReadAsArray()

                # Normalize the array to 0-255
                if np.any(array != array.min()):
                    array_normalized = ((array - array.min()) / (array.max() - array.min()) * 255).astype(np.uint8)
                else:
                    array_normalized = np.zeros_like(array, dtype=np.uint8)

                # Convert the normalized array to QImage
                height, width = array_normalized.shape
                bytesPerLine = width
                image = QImage(array_normalized.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)

            # Scale QImage to fit the current window size while maintaining aspect ratio
            image_scaled = image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Set QImage as the pixmap of QLabel
            self.imageLabel.setPixmap(QPixmap.fromImage(image_scaled))

            self.setWindowTitle(f"Image Window - {imagePath}")
            logging.info(f"{self.displayMode} Image {imagePath} displayed successfully.")
        except Exception as e:
            logging.error(f"Error loading and displaying {self.displayMode} image: %s", str(e), exc_info=True)
            QMessageBox.critical(self, "Error", f"An error occurred while loading or displaying the {self.displayMode} image.")

    def populateBandSelectionDropdowns(self, imagePath):
        hdrPath = imagePath.rsplit('.', 1)[0] + '.hdr'  # More robust handling of file extension replacement
        if os.path.exists(hdrPath):
            try:
                hdr = spectral.envi.open(hdrPath)
                band_names = hdr.bands.names
                self.redBandComboBox.clear()
                self.greenBandComboBox.clear()
                self.blueBandComboBox.clear()
                for name in band_names:
                    self.redBandComboBox.addItem(name)
                    self.greenBandComboBox.addItem(name)
                    self.blueBandComboBox.addItem(name)
            except Exception as e:
                logging.error("Error populating band selection dropdowns with band names: %s", str(e), exc_info=True)
        else:
            # Fallback to default behavior if HDR file is not found or band names are not available
            self.redBandComboBox.clear()
            self.greenBandComboBox.clear()
            self.blueBandComboBox.clear()
            for i in range(1, self.dataset.RasterCount + 1):
                bandStr = str(i)
                self.redBandComboBox.addItem(bandStr)
                self.greenBandComboBox.addItem(bandStr)
                self.blueBandComboBox.addItem(bandStr)

    def applySelectedBands(self):
        try:
            redBand = int(self.redBandComboBox.currentText())
            greenBand = int(self.greenBandComboBox.currentText())
            blueBand = int(self.blueBandComboBox.currentText())
            self.loadAndDisplayImage(self.dataset.GetDescription(), bands=[redBand, greenBand, blueBand], displayMode='RGB')
            logging.info("RGB bands applied successfully.")
        except Exception as e:
            logging.error("Error applying RGB bands: %s", str(e), exc_info=True)
            QMessageBox.critical(self, "Error", "An error occurred while applying RGB bands.")

    def mouseMoveEvent(self, event):
        try:
            x, y = event.pos().x(), event.pos().y()
            # Convert pixel coordinates to geospatial coordinates
            gt = self.dataset.GetGeoTransform()
            geo_x = gt[0] + x * gt[1] + y * gt[2]
            geo_y = gt[3] + x * gt[4] + y * gt[5]
            self.statusBar.showMessage(f"Latitude: {geo_y}, Longitude: {geo_x}")
            logging.info(f"Mouse moved to Latitude: {geo_y}, Longitude: {geo_x}")
        except Exception as e:
            logging.error("Error processing mouse movement: %s", str(e), exc_info=True)
            QMessageBox.critical(self, "Error", "An error occurred while processing mouse movement.")