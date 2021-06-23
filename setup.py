from setuptools import setup

setup(
    name='accounting_cli',
    version='1.0',
    py_modules=['accounting_cli'],
    packages=['lib'],
    entry_points={
        'console_scripts': [
            'accounting_cli=accounting_cli:main'
        ]
    }
)