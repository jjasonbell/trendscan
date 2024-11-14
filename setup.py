from setuptools import setup, find_packages

setup(
    name="trendscan",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",  
        "python-dotenv",
        "langdetect",
        "serpapi" 
    ],
    entry_points={
        "console_scripts": [
            "trendscan=trendscan.main:main",  # Example for a CLI command, if you have a `main.py`
        ],
    },
    # Additional metadata
    description="A package for spotting trends, market research, and validation",
    author="J. Jason Bell",
    author_email="jason.bell@sbs.ox.ac.uk",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)