import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("src/usdm_info/__init__.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="usdm",
    version=version["__package_version__"],
    author="D Iberson-Hurst",
    author_email="",
    description="A python package for using the CDISC TransCelerate USDM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "beautifulsoup4>=4.9",
        "openpyxl>=3.0",
        "pandas>=1.5",
        "pydantic>=2.0",
        "pyyaml>=5.1",
        "requests>=2.25",
        "yattag>=1.14",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"usdm_excel": ["data/*.yaml", "data/*.json"]},
    tests_require=["pytest"],
    python_requires=">=3.12",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)
