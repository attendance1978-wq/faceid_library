# Update setup.py with corrected information
@"
\"\"\"
Setup script for faceid library
\"\"\"

from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

setup(
    name="faceid",
    version="1.0.0",
    author="attendance1978-wq",
    author_email="attendance1978-wq@users.noreply.github.com",
    description="Advanced Face Recognition and Identification Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/attendance1978-wq/faceid_library",
    project_urls={
        "Bug Reports": "https://github.com/attendance1978-wq/faceid_library/issues",
        "Source": "https://github.com/attendance1978-wq/faceid_library",
    },
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "faceid-demo=faceid.demo:run_demo",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
"@ | Out-File -FilePath setup.py -Encoding UTF8
