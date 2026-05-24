"""
Setup script for faceid library
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="faceid",
    version="1.0.0",
    author="FaceID Team",
    author_email="support@faceid.com",
    description="Advanced Face Recognition and Identification Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/faceid/faceid",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
        "gpu": [
            "tensorflow-gpu>=2.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "faceid-demo=faceid.demo:run_demo",
        ],
    },
)
