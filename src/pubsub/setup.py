from setuptools import find_packages, setup

package_name = 'pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rss',
    maintainer_email='rss@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [ 'publisher_node = pubsub.publisher:main', 
                             'subscriber_node = pubsub.sub:main',
                             'subscriber_node2 = pubsub.sub2:main' 
        ],
    },
)
