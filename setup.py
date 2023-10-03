from setuptools import setup, find_packages

setup(
    name='fuzzy-youtube_downloader',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'yt_downloader = yt_downloader.gui:main'
        ]
    },
    install_requires=[
        'pytube',
        'PyGObject'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
