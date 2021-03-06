from setuptools import setup
import os
from glob import glob
package_name = 'python_gui'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'xml'), glob('xml/*.xml')),
        (os.path.join('share', package_name, 'json'), glob('json/*.json')),
        (os.path.join('share', package_name, 'icons'), glob('icons/es_ico.png')),
        (os.path.join('share', package_name, 'test_deploy'), glob('test_deploy/*.lua')),
        (os.path.join('share', package_name, 'lua_components'), glob('lua_components/*.lua')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gborghesan',
    maintainer_email='gianni.borghesan@kuleuven.be',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'gui_sender = python_gui.gui_sender:main',
        ],
    },
)
