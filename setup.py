from setuptools import setup, find_packages

setup(
    name="phindllama",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'web3',
        'pandas',
        'streamlit'
    ],
)
