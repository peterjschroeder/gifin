#!/usr/bin/env python3

from distutils.core import setup

setup(
        name='gifin', 
        version='0.1', 
        description='gif selector that outputs to WeeChat.', 
        author='Peter J. Schroeder', 
        author_email='peterjschroeder@gmail.com', 
        url='https://github.com/peterjschroeder/gifin',
        scripts=['gifin'],
        install_requires=['term-image @ git+https://github.com/AnonymouX47/term-image.git']
)

