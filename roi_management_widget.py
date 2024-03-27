from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableView, QHeaderView, QHBoxLayout, QDialog, QLineEdit, QLabel, QFormLayout, QMessageBox, QColorDialog
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QColor

class RoiTableModel(QAbstractTableModel):
    def __init__(self, rois=None):
        super().__init__()
        self.rois = rois or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            roi = self.rois[index.row()]
            return roi[index.column()]

    def rowCount(self, index):
        return len(self.rois)

    def columnCount(self, index):
        return 3  # Now includes 'Name', 'Notes', and 'Color'

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["Name", "Notes", "Color"][section]

    def addRoi(self, roi):
        self.beginInsertRows(QModelIndex(), len(self.rois), len(self.rois))
        self.rois.append(roi)
        self.endInsertRows()

    def editRoi(self, row, roi):
        if 0 <= row < len(self.rois):
            self.rois[row] = roi
            self.dataChanged.emit(self.index(row, 0), self.index(row, len(roi)-1), [Qt.DisplayRole])

    def removeRoi(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.rois[row]
        self.endRemoveRows()


class RoiManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.tableModel = RoiTableModel([["Sample ROI", "No notes yet", "#ff0000"]])  # Default color red
        self.tableView = QTableView()
        self.tableView.setModel(self.tableModel)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.tableView)

        # Buttons for adding, editing, and deleting ROIs
        self.buttonsLayout = QHBoxLayout()
        self.addButton = QPushButton("Add")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.editButton)
        self.buttonsLayout.addWidget(self.deleteButton)
        self.layout.addLayout(self.buttonsLayout)

        self.addButton.clicked.connect(self.addRoi)
        self.editButton.clicked.connect(self.editRoi)
        self.deleteButton.clicked.connect(self.deleteRoi)

        self.setLayout(self.layout)

    def addRoi(self):
        dialog = RoiDialog()
        if dialog.exec_():
            self.tableModel.addRoi([dialog.nameEdit.text(), dialog.notesEdit.text(), dialog.color.name()])
            print("ROI added")

    def editRoi(self):
        row = self.tableView.currentIndex().row()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select an ROI to edit.")
            return
        roi = self.tableModel.rois[row]
        dialog = RoiDialog(roi)
        if dialog.exec_():
            self.tableModel.editRoi(row, [dialog.nameEdit.text(), dialog.notesEdit.text(), dialog.color.name()])
            print("ROI edited")

    def deleteRoi(self):
        row = self.tableView.currentIndex().row()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select an ROI to delete.")
            return
        self.tableModel.removeRoi(row)
        print("ROI deleted")


class RoiDialog(QDialog):
    def __init__(self, roi=None):
        super().__init__()
        self.setWindowTitle("ROI Details")
        self.layout = QFormLayout()
        self.nameEdit = QLineEdit(roi[0] if roi else "")
        self.notesEdit = QLineEdit(roi[1] if roi else "")
        self.colorEdit = QPushButton("Select Color")
        self.color = QColor(roi[2] if roi else "#ff0000")  # Default color red
        self.colorEdit.setStyleSheet("background-color: %s;" % self.color.name())
        self.colorEdit.clicked.connect(self.selectColor)
        self.layout.addRow(QLabel("Name:"), self.nameEdit)
        self.layout.addRow(QLabel("Notes:"), self.notesEdit)
        self.layout.addRow(QLabel("Color:"), self.colorEdit)
        self.buttonsLayout = QHBoxLayout()
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.buttonsLayout.addWidget(self.okButton)
        self.buttonsLayout.addWidget(self.cancelButton)
        self.layout.addRow(self.buttonsLayout)
        self.setLayout(self.layout)

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def selectColor(self):
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.colorEdit.setStyleSheet("background-color: %s;" % color.name())

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    widget = RoiManagementWidget()
    widget.show()
    sys.exit(app.exec_())