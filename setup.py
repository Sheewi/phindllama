from setuptools import setup, find_packages

setup(
    name="phindllama",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'web3>=6.0.0',
        'pandas>=1.5.0',
        'streamlit>=1.20.0',
        'pydantic>=2.0.0',
        'questionary>=1.10.0',
        'fastapi>=0.100.0',
        'uvicorn>=0.20.0',
        'PyYAML>=6.0',
        'boto3>=1.26.0',
        'scikit-learn>=1.3.0',
        'requests>=2.28.0',
        'redis>=4.5.0',
        'python-dotenv>=1.0.0',
        'opentelemetry-api>=1.15.0',
        'opentelemetry-sdk>=1.15.0',
        'cryptography>=41.0.0',
        'websockets>=11.0.0',
        'aiohttp>=3.8.0',
        'sqlalchemy>=2.0.0',
        'psycopg2-binary>=2.9.0',
        'transformers>=4.30.0',
        'torch>=2.0.0',
        'numpy>=1.24.0'
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'phindllama=phindllama.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
