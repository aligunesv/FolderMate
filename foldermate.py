import os
import mimetypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QLineEdit, QPushButton, QTextBrowser, QDesktopWidget
from PyQt5.QtGui import QDesktopServices, QPixmap, QColor, QPalette
from PyQt5.QtCore import QUrl

class FolderMate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FolderMate")
        self.setGeometry(100, 100, 500, 500)
        self.setFixedSize(500, 500)

        self.palette = QPalette()
        self.palette.setColor(QPalette.Background, QColor("#212A3E"))
        self.setPalette(self.palette)

        self.label1 = QLabel("Select Folders to Search:", self)
        self.label1.setGeometry(20, 20, 200, 25)
        self.label1.setStyleSheet("color: #F1F6F9;")

        self.folder_path = QLineEdit(self)
        self.folder_path.setGeometry(20, 50, 365, 25)
        self.folder_path.setStyleSheet("background-color: #F1F6F9; color: #0b0b0b; border-radius: 5px;")

        self.browse_btn = QPushButton("Browse", self)
        self.browse_btn.setGeometry(400, 50, 80, 25)
        self.browse_btn.setStyleSheet("background-color: #9BA4B5; color: #212A3E;  border-radius: 5px;")

        self.label2 = QLabel("Filter by File Type:", self)
        self.label2.setGeometry(20, 100, 200, 25)
        self.label2.setStyleSheet("color: #F1F6F9;")

        self.file_type = QLineEdit(self)
        self.file_type.setGeometry(20, 130, 365, 25)
        self.file_type.setStyleSheet("background-color: #F1F6F9; color: #0b0b0b; border-radius: 5px;")

        self.search_btn = QPushButton("Search", self)
        self.search_btn.setGeometry(400, 130, 80, 25)
        self.search_btn.setStyleSheet("background-color: #9BA4B5; color: #212A3E; border-radius: 5px;")

        self.result_label = QLabel("Search Results:", self)
        self.result_label.setGeometry(20, 180, 200, 25)
        self.result_label.setStyleSheet("color: #F1F6F9;")

        self.result_text = QTextBrowser(self)
        self.result_text.setGeometry(20, 210, 460, 250)
        self.result_text.setStyleSheet("background-color: #F1F6F9; color: #0b0b0b; border-radius: 5px;")
        self.result_text.anchorClicked.connect(self.open_file)

        self.browse_btn.clicked.connect(self.browse_folder)
        self.search_btn.clicked.connect(self.search_files)

        self.show()

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.folder_path.setText(folder)

    def search_files(self):
        folder_path = self.folder_path.text()
        file_type = self.file_type.text()

        self.result_text.clear()
        if not os.path.isdir(folder_path):
            self.result_text.setText("Please select a valid folder!")
        else:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(file_type):
                        file_path = os.path.join(root, file)
                        self.result_text.append('<a href="{}">{}</a>'.format(file_path, file))


    def open_file(self, url):
        file_path = url.path()[1:]
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith('image'):
            pixmap = QPixmap(file_path)
            self.image_viewer = QLabel()
            self.image_viewer.setPixmap(pixmap)
            self.image_viewer.setGeometry(0, 0, pixmap.width(), pixmap.height())
            self.image_viewer.setWindowTitle(file_path)
            self.image_viewer.show()
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(file_path)))


if __name__ == '__main__':
    app = QApplication([])
    foldermate = FolderMate()
    app.exec_()
