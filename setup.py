"""Package configuration"""
from setuptools import setup, find_packages

# Package metadata
NAME = "Earthquake Research"
VERSION = "0.1.0"
AUTHOR = "Carrow Morris-Wiltshre, Aleksandra Zaforemska, Kristina Wolf"
EMAIL = "c.morris-wiltshire@newcastle.ac.uk, a.zaforemska2@newcastle.ac.uk, k.wolf2@newcastle.ac.uk"
DESCRIPTION = "Backend for Earthquake Research using ArcMap"
URL = "https://github.com/alekszaf/EarthquakeMetadata.git"

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

# Setuptools configuration
setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="earthquake research",
    install_requires=["google-auth", "google-cloud-storage", "pandas"],
    python_requires=">=3.10",
)
