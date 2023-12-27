import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QTimer, Qt, QLibraryInfo


os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(            # 解决linux环境下Qt和CV的插件冲突
    QLibraryInfo.PluginsPath
)

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("相机应用")
        self.setGeometry(100, 100, 640, 480)

        # 创建布局
        main_layout = QVBoxLayout()

        # 创建拍照按钮
        self.capture_button = QPushButton("拍照", self)
        self.capture_button.setFixedSize(210, 40)           # 设置按钮宽度为318
        self.capture_button.clicked.connect(self.capture_image)

        # 创建保存按钮
        self.save_button = QPushButton("保存", self)
        self.save_button.setFixedSize(210, 40)
        self.save_button.clicked.connect(self.save_image)

        # 创建选择照片按钮
        self.select_button = QPushButton("选择照片", self)
        self.select_button.setFixedSize(210, 40)
        self.select_button.clicked.connect(self.select_photo)

        # 创建用于显示相机图像的标签
        self.camera_label = QLabel(self)

        # 创建用于显示照片的标签
        self.photo_label = QLabel(self)
        placeholder_pixmap = QPixmap(640, 480)
        placeholder_pixmap.fill(Qt.lightGray)           # 初始时使用浅灰色填充
        self.photo_label.setPixmap(placeholder_pixmap)

        # 创建水平布局，包含相机图像标签和照片标签
        camera_layout = QHBoxLayout()
        camera_layout.addWidget(self.camera_label)

        photo_layout = QHBoxLayout()
        photo_layout.addWidget(self.photo_label)

        # 创建水平布局，包含保存按钮、拍照按钮、选择按钮
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.capture_button)        
        input_layout.addWidget(self.save_button)
        input_layout.addWidget(self.select_button)

        # 将布局添加到垂直布局
        main_layout.addLayout(camera_layout)
        main_layout.addLayout(photo_layout)
        main_layout.addLayout(input_layout)

        # 设置水平布局对齐方式为左对齐
        input_layout.setAlignment(Qt.AlignLeft)

        # 创建计时器，用于定期刷新显示的相机图像
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_image)

        # 初始化相机
        camera_index = self.find_camera_index()                         # 获取相机id
        if camera_index is not None:
            self.cap = cv2.VideoCapture(camera_index)
            print("Camera_index:", camera_index ,", Camera launch successfully.")
            # 进行后续操作
        else:
            print("No camera found.")

        # 创建人脸检测器
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # 启动计时器，每10毫秒更新一次相机图像
        self.timer.start(10)

        # 设置布局
        self.setLayout(main_layout)

    def find_camera_index(self):
        """ 查找相机设备id """
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cap.release()
                return i
        return None

    def capture_image(self):
        """ 拍照按钮功能 """
        # 读取当前帧
        ret, frame = self.cap.read()

        # 将图像转换为Qt图像
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qt_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # 显示拍摄的照片
        self.photo_label.setPixmap(QPixmap.fromImage(qt_image))

        # 已拍摄的图像
        self.captured_image = image             # 保存拍摄的照片

    def update_camera_image(self):
        """ 刷新相机界面 """
        # 定期刷新显示的相机图像
        ret, frame = self.cap.read()

        # 在图像中检测人脸
        faces = self.detect_faces(frame)

        # 在图像上绘制人脸框
        for (x, y, w, h) in faces:
            # 调整人脸框的大小
            x, y, w, h = int(x + 0.1 * w), int(y + 0.1 * h), int(0.8 * w), int(0.8 * h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # 将图像转换为Qt图像
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qt_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # 显示相机图像
        self.camera_label.setPixmap(QPixmap.fromImage(qt_image))

    def save_image(self):
        """ 保存图片 """
        # 弹出文件保存对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path, _ = QFileDialog.getSaveFileName(self, "请选择保存位置", "", "JPEG 图像 (*.jpg);;所有文件 (*)", options=options)

        # 如果用户选择了保存位置，保存图像
        if folder_path:
            file_path = folder_path + ".jpg"
            cv2.imwrite(file_path, cv2.cvtColor(self.captured_image, cv2.COLOR_RGB2BGR))
            print(f'图像已保存到：{file_path}')

    def select_photo(self):
        """ 选择照片 """
        # 弹出文件选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "选择照片", "", "图片文件 (*.png *.jpg *.bmp);;所有文件 (*)", options=options)

        # 如果用户选择了照片，显示在图片标签中
        if file_path:
            # 读取照片
            image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
            # 将图像转换为Qt图像
            qt_image = QImage(image.data, image.shape[1], image.shape[0], image.shape[1] * 3, QImage.Format_RGB888)
            # 显示照片
            self.photo_label.setPixmap(QPixmap.fromImage(qt_image))

        # 已加载的图像
        self.captured_image = image

    def detect_faces(self, frame):
        """ 在图像中检测人脸 """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def closeEvent(self, event):
        # 关闭窗口时释放相机资源
        self.cap.release()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera_app = CameraApp()
    camera_app.show()
    sys.exit(app.exec_())
