from setuptools import setup

package_name = 'pyqt_realsense'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],  # This is your package directory
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
        'pyrealsense2',  # RealSense SDK
        'PyQt5',          # PyQt5 for GUI
        'rclpy',          # ROS 2 Python library
    ],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='PyQt5 application for RealSense in ROS 2',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'viewer = pyqt_realsense.viewer:main',  # Update if main() is the entry point
        ],
    },
)
