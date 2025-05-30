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
        "pandas",
        "openpyxl",
        "pydantic",
        "requests",
        "stringcase",
        "yattag",
        "docraptor",
        "beautifulsoup4",
        "pyyaml",
        "fhir.resources",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"usdm_excel": ["data/*.yaml", "data/*.json"]},
    tests_require=["pytest"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
