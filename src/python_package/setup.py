import os

from setuptools import find_packages, setup
from glob import glob


package_name = 'python_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rss',
    maintainer_email='kkk@ad.fh-aachen.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['emptynode = python_package.first_node:main', 
                            'param_node = python_package.param_node:main'
        ],
    },
)
