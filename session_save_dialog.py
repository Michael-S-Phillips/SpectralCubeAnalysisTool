from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel

class SessionSaveDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save Session")
        layout = QVBoxLayout()

        self.filenameEdit = QLineEdit()
        layout.addWidget(QLabel("Filename:"))
        layout.addWidget(self.filenameEdit)

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.accept)
        layout.addWidget(saveButton)

        self.setLayout(layout)

    def getFilename(self):
        return self.filenameEdit.text()