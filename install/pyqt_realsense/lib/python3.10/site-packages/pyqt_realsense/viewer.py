import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage
import pyrealsense2 as rs
import numpy as np
import rclpy
from rclpy.node import Node

class Viewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.setup_ui()

        # RealSense components
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # Timer for frame updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_frames)
        self.timer.start(33)  # ~30 fps

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        # Left side
        left_layout = QVBoxLayout()
        self.color_view = QLabel("No Camera Feed")
        self.color_view.setMinimumSize(640, 480)
        self.color_view.setAlignment(Qt.AlignCenter)
        self.start_button = QPushButton("Start Camera")
        self.start_button.clicked.connect(self.handle_start_button)

        left_layout.addWidget(self.color_view)
        left_layout.addWidget(self.start_button)

        main_layout.addLayout(left_layout)

        self.setWindowTitle("RealSense Viewer")
        self.resize(1300, 600)

    def handle_start_button(self):
        if not self.is_running:
            try:
                self.config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
                self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
                self.pipeline.start(self.config)
                self.is_running = True
                self.start_button.setText("Stop Camera")
            except Exception as e:
                print(f"Failed to start camera: {e}")
        else:
            self.pipeline.stop()
            self.is_running = False
            self.start_button.setText("Start Camera")
            self.color_view.setText("No Camera Feed")

    def convert_color_to_qimage(self, frame):
        data = np.asanyarray(frame.get_data())
        height, width, channels = data.shape
        return QImage(data, width, height, QImage.Format_RGB888).copy()

    def process_frames(self):
        if not self.is_running:
            return

        try:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            if color_frame:
                image = self.convert_color_to_qimage(color_frame)
                self.color_view.setPixmap(QPixmap.fromImage(image))
            else:
                print("No color frame captured.")

        except Exception as e:
            print(f"Frame capture error: {e}")

def main(args=None):
    rclpy.init(args=args)  # ROS 2 initialization
    app = QApplication(sys.argv)
    viewer = Viewer()
    viewer.show()
    result = app.exec()
    rclpy.shutdown()  # ROS 2 shutdown
    sys.exit(result)

if __name__ == "__main__":
    main()
