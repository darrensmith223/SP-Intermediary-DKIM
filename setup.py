from setuptools import setup, find_packages


setup(
    name='spdkim',
    version='0.1',
    author='Darren Smith',
    author_email='darren.smith@sparkpost.com',
    packages=find_packages(),
    url='https://github.com/darrensmith223/SP-Intermediary-DKIM',
    license='Apache 2.0',
    description='Configure Intermediary DKIM Domain with SparkPost',
    install_requires=['requests>=2.20.1']
)