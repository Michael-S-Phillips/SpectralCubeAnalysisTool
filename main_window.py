from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog
from roi_management_widget import RoiManagementWidget
from session_save_dialog import SessionSaveDialog
from image_management_window import ImageManagementWindow
from relab_integration import RelabIntegrationWidget
from osgeo import gdal
import sys
import pickle

# Enable GDAL's exception mechanism
gdal.UseExceptions()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo_app - Hyperspectral Image Analysis")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        self.initUI()
    
    def initUI(self):
        menu_bar = self.menuBar()
        # Check if the application is running on macOS and adjust menu bar accordingly
        if sys.platform == "darwin":
            menu_bar.setNativeMenuBar(False)
        self.fileMenu = menu_bar.addMenu('&File')
        self.helpMenu = menu_bar.addMenu('&Help')

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QApplication.instance().quit)

        aboutAction = QAction('&About', self)
        aboutAction.triggered.connect(lambda: print("About clicked"))

        self.fileMenu.addAction(exitAction)
        self.helpMenu.addAction(aboutAction)

        self.initSessionManagement()
        self.initImageManagement()
        self.initRelabIntegration()

        self.roiManagementWidget = RoiManagementWidget()
        self.setCentralWidget(self.roiManagementWidget)

    def initSessionManagement(self):
        saveSessionAction = QAction('&Save Session', self)
        saveSessionAction.triggered.connect(self.saveSession)
        loadSessionAction = QAction('&Load Session', self)
        loadSessionAction.triggered.connect(self.loadSession)
        self.fileMenu.addAction(saveSessionAction)
        self.fileMenu.addAction(loadSessionAction)

    def initImageManagement(self):
        imageManagementAction = QAction('&Image Management', self)
        imageManagementAction.triggered.connect(self.openImageManagementWindow)
        self.fileMenu.addAction(imageManagementAction)

    def initRelabIntegration(self):
        relabIntegrationAction = QAction('&RELAB Database', self)
        relabIntegrationAction.triggered.connect(self.openRelabIntegrationWindow)
        self.fileMenu.addAction(relabIntegrationAction)

    def openImageManagementWindow(self):
        self.imageManagementWindow = ImageManagementWindow()
        self.imageManagementWindow.show()

    def openRelabIntegrationWindow(self):
        self.relabIntegrationWindow = RelabIntegrationWidget()
        self.relabIntegrationWindow.show()

    def saveSession(self):
        dialog = SessionSaveDialog()
        if dialog.exec_():
            filename = dialog.getFilename()
            if filename:
                if not filename.endswith('.session'):
                    filename += '.session'
                try:
                    session_data = {
                        'rois': self.roiManagementWidget.tableModel.rois,
                        # Add other session states as needed
                    }
                    with open(filename, 'wb') as file:
                        pickle.dump(session_data, file)
                    print("Session saved")
                except Exception as e:
                    print(f"Error saving session: {e}")

    def loadSession(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Session", "", "Session Files (*.session)")
        if filename:
            try:
                with open(filename, 'rb') as file:
                    session_data = pickle.load(file)
                    self.roiManagementWidget.tableModel.rois = session_data['rois']
                    self.roiManagementWidget.tableModel.layoutChanged.emit()
                    # Add other states loading as needed
                    print("Session loaded")
            except Exception as e:
                print(f"Error loading session: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())