from setuptools import setup, find_packages

setup(
    name='text_snake',
    version='0.1',
    author='Ninja00Shadow',
    url='https://github.com/Ninja00Shadow/text_snake',
    packages=find_packages(),
    install_requires=[
        'blessed',
    ],
    entry_points={
        'console_scripts': [
            'snake = text_snake.main:main',
        ],
    },
)
