import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSplitter, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from model import ModelViewer
from camera import CameraApp

class IntegratedApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("Picture to Model")
        self.setGeometry(100, 100, 1280, 960)

        # 创建主布局
        main_layout = QHBoxLayout()

        # 创建左侧布局
        left_layout = QVBoxLayout()

        # 添加相机应用到左侧布局
        self.camera_app = CameraApp()
        left_layout.addWidget(self.camera_app)

        # 创建右侧布局
        right_layout = QVBoxLayout()

        # 添加模型查看器到右侧布局
        self.model_viewer = ModelViewer()
        right_layout.addWidget(self.model_viewer)

        # 创建按钮布局
        button_layout = QVBoxLayout()

        # 创建一个弹簧，使得按钮位于两个模块中间
        spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        button_layout.addItem(spacer)

        # 中间添加一个按钮
        reconstruct_button = QPushButton("三维重建", self)
        reconstruct_button.clicked.connect(self.reconstruct_3d)

        # 按钮字体设置
        font = reconstruct_button.font()
        font.setPointSize(16)               # 设置字体大小为16
        font.setBold(True)                  # 设置字体加粗
        reconstruct_button.setFont(font)

        button_layout.addWidget(reconstruct_button)

        # 创建一个弹簧，使得按钮位于两个模块中间
        spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        button_layout.addItem(spacer)

        # 将左侧、按钮和右侧布局添加到主布局
        main_layout.addLayout(left_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(right_layout)

        # 设置主窗口的布局
        self.setLayout(main_layout)

    def reconstruct_3d(self):
        """ 触发三维重建的代码 """
        print("进行三维重建")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    integrated_app = IntegratedApp()
    integrated_app.show()
    sys.exit(app.exec_())
