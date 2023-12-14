import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap

class PhotoViewer(QMainWindow):
    def __init__(self):
        super(PhotoViewer, self).__init__()

        self.setWindowTitle("照片查看器")
        self.setGeometry(100, 100, 800, 600)

        # 创建 QLabel 用于显示照片
        self.photo_label = QLabel(self)
        self.photo_label.setAlignment(Qt.AlignCenter)

        # 创建 QPushButton 用于选择照片
        self.select_button = QPushButton("选择照片", self)
        self.select_button.clicked.connect(self.select_photo)

        # 创建 QVBoxLayout 用于布局
        layout = QVBoxLayout()
        layout.addWidget(self.photo_label)
        layout.addWidget(self.select_button)

        # 创建 QWidget 作为主窗口的中心部件
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_photo(self):
        # 弹出文件选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "选择照片", "", "图像文件 (*.png *.jpg *.bmp *.gif);;所有文件 (*)", options=options)

        # 如果选择了文件，显示照片
        if file_name:
            pixmap = QPixmap(file_name)
            self.photo_label.setPixmap(pixmap)
            self.photo_label.adjustSize()  # 调整标签大小以适应图像

if __name__ == '__main__':
    app = QApplication(sys.argv)
    photo_viewer = PhotoViewer()
    photo_viewer.show()
    sys.exit(app.exec_())
