"""Boilerplate setup for a WECS-based game.
"""

from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

setup(
    name='wecs-null-project',  # STARTPROJECT: Package name
    version='0.0.1a',
    description='',   # STARTPROJECT: Short package description
    url='',  # STARTPROJECT
    author='',  # STARTPROJECT
    author_email='',  # STARTPROJECT
    classifiers=[
        'Development Status :: 3 - Alpha',  # STARTPROJECT
    ],
    keywords='',  # STARTPROJECT: Package keywords
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.7, <4',
    install_requires=[
        'wecs',
        'panda3d',
        'panda3d-keybindings',
    ],
    entry_points={
        'console_scripts': [
            'game_name=main:run_game',  # STARTPROJECT: Change game_name
        ],
    },
    # Deployment
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.bam',
                '**/*.toml',
            ],
            'include_modules': {
                '*': [
                    'keybindings',
                ],
            },
            'gui_apps': {
                'default_name': 'main.py',  # STARTPROJECT
            },
            'log_filename': '$USER_APPDATA/default_name/output.log',  # STARTPROJECT
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
            'platforms': [  # STARTPROJECT: Change selection
                'manylinux1_x86_64',
                #'macosx_10_6_x86_64',
                #'win_amd64',
            ],
        },
    },
)
