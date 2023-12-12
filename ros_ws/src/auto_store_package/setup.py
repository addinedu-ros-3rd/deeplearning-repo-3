from setuptools import find_packages, setup
import glob, os

package_name = 'auto_store_package'

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
    maintainer='cho',
    maintainer_email='whghdrl9977@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'auto_store_publisher = auto_store_package.auto_store_publisher:main',
            'auto_store_subscriber_1 = auto_store_package.auto_store_subscriber_1:main',
            'auto_store_subscriber_2 = auto_store_package.auto_store_subscriber_2:main',
            'auto_store_subscriber_two = auto_store_package.auto_store_subscriber_two:main'
        ],
    },
)
