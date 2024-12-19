import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/thornch/ROS2_Repo/pyqt_realsense/install/pyqt_realsense'
